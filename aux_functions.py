"""This module contains auxiliary functions for soccermatics project."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch, VerticalPitch
import pandas as pd
import numpy as np

background_color = "#1b1b1b"
text_color = "white"
mpl.rcParams["figure.facecolor"] = background_color
mpl.rcParams["axes.facecolor"] = background_color
# mpl.rcParams["font.family"] = "Alegreya Sans"
team1_color = "#f99f84"
team2_color = "#84def9"


def reset_matplotlib():
    """Reset the matplotlib rcParams to their default values."""
    mpl.rcParams.update(mpl.rcParamsDefault)


def plot_shots_1team(df, team=""):
    """
    Plot the shots of a given team in a vertical pitch.

    Args:
    - df: pandas DataFrame containing the data to be plotted.
    - team: string representing the name of the team to be plotted.

    Returns:
    - None
    """
    # test for valid inputs
    if team == " ":
        raise ValueError("Please enter team name")
    # create pitch to plot
    pitch = VerticalPitch(
        pitch_type="statsbomb",
        line_color="grey",
        pitch_color="#1b1b1b",
        half=True,
    )
    fig, ax = pitch.draw(figsize=(8, 5))
    # create df_shots
    df_shots = df[(df["type"] == "Shot") & (df["team"] == team)].copy()
    # unpack location variable
    df_shots[["position_x", "position_y"]] = pd.DataFrame(
        df_shots.location.tolist(), index=df_shots.index
    )
    # iterate over rows to plot shots

    for i, shot in df_shots.iterrows():
        x = shot["position_x"]
        y = shot["position_y"]
        goal = shot["shot_outcome"] == "Goal"
        # marker_size_xg = shot["shot_statsbomb_xg"]
        marker_size = 2
        if goal:
            shot_circle = plt.Circle((x, y), marker_size, color="#f99f84")
            plt.text(
                x + 1,
                y - 2,
                shot["player"].split(" ")[-1],
                fontsize=8,
                color="white",
            )
        else:
            shot_circle = plt.Circle((x, y), marker_size, color="#f99f84")
            shot_circle.set_alpha(0.5)
        # xg_circle = plt.Circle((x, y), marker_size_xg, color="white")
        ax.add_patch(shot_circle)
        # ax.add_patch(xg_circle)


def plot_shots_2teams(df):
    """
    Plot the shots of two teams in a pitch.

    Args:
    - df: pandas DataFrame containing the data to be plotted.

    Returns:
    - None
    """
    # create pitch to plot
    pitch = Pitch(
        pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b"
    )
    fig, ax = pitch.draw(figsize=(8, 5))  # type: ignore
    # get teams names
    team1, team2 = df["team"].unique()
    # create df_shots
    df_shots = df[df["type"] == "Shot"].copy()
    # unpack location variable
    df_shots[["position_x", "position_y"]] = pd.DataFrame(
        df_shots.location.tolist(), index=df_shots.index
    )
    # iterate over rows to plot shots
    # TODO: find a way to avoid using iterrows
    for i, shot in df_shots.iterrows():
        x = shot["position_x"]
        y = shot["position_y"]
        goal = shot["shot_outcome"] == "Goal"
        team_name = shot["team"]
        # TODO: find a elegant way to integrate xg into the shots plot
        # marker_size_xg = shot["shot_statsbomb_xg"]
        marker_size = 2
        if team_name == team1:
            if goal:
                shot_circle = plt.Circle((x, y), marker_size, color="#f99f84")
                plt.text(
                    x + 1,
                    y - 2,
                    shot["player"].split(" ")[-1],
                    fontsize=8,
                    color="white",
                )
            else:
                shot_circle = plt.Circle((x, y), marker_size, color="#f99f84")
                shot_circle.set_alpha(0.5)
            # xg_circle = plt.Circle((x, y), marker_size_xg, color="white")
        # TODO: define default numbers for pitch dimensions
        elif team_name == team2:
            if goal:
                shot_circle = plt.Circle(
                    (120 - x, 80 - y), marker_size, color="#84def9"
                )
                plt.text(
                    120 - x + 1,
                    80 - y - 2,
                    shot["player"].split(" ")[-1],
                    fontsize=8,
                    color="white",
                )
            else:
                shot_circle = plt.Circle(
                    (120 - x, 80 - y), marker_size, color="#84def9"
                )
                shot_circle.set_alpha(0.5)
            # xg_circle = plt.Circle(
            #     (120 - x, 80 - y), marker_size_xg, color="w"
            # )
        ax.add_patch(shot_circle)
        # ax.add_patch(xg_circle)


def plot_passes_arrow(df, team=" ", player=" "):
    """
    Plot arrows representing passes between players in a soccer match.

    Args:
    - df: pandas DataFrame containing the data to be plotted.
    - team: string representing the name of the team to be plotted.
    Default is an empty string.
    - player: string representing the name of the player to be plotted.
    Default is an empty string.

    Returns:
    - None
    """
    # test for valid inputs
    if team == " " and player == " ":
        raise ValueError("Please enter either team or player name")
    elif team != " " and player != " ":
        raise ValueError("Please enter only team or player name")
    # create pitch to plot
    pitch = Pitch(
        pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b"
    )
    fig, ax = pitch.draw(figsize=(10, 6))
    # create df_pass
    df_pass = df[
        (df["type"].isin(["Pass"]))
        & (df["pass_type"].isin([np.nan, "Goal Kick"]))
    ].copy()
    # unpack location variable
    df_pass[["position_x", "position_y"]] = pd.DataFrame(
        df_pass.location.tolist(), index=df_pass.index
    )
    # unpack pass_end_location variable
    df_pass[["end_pass_x", "end_pass_y"]] = pd.DataFrame(
        df_pass.pass_end_location.tolist(), index=df_pass.index
    )
    # filter df_pass
    if team != " ":
        df_pass = df_pass[df_pass["team"] == team]
    elif player != " ":
        df_pass = df_pass[df_pass["player"] == player]
    else:
        raise ValueError("Please follow the instructions")
    # separate completed passes from other passes
    df_pass_completed = df_pass[df_pass.pass_outcome.isna()]
    df_pass_other = df_pass[~df_pass.pass_outcome.isna()]
    # plot completed passes
    pitch.arrows(
        df_pass_completed.position_x,
        df_pass_completed.position_y,
        df_pass_completed.end_pass_x,
        df_pass_completed.end_pass_y,
        ax=ax,
        color="green",
        width=2,
        headwidth=4,
        headlength=4,
    )
    # plot other passes
    pitch.arrows(
        df_pass_other.position_x,
        df_pass_other.position_y,
        df_pass_other.end_pass_x,
        df_pass_other.end_pass_y,
        ax=ax,
        color="red",
        width=2,
        headwidth=4,
        headlength=4,
    )
    # plot players positions
    pitch.scatter(
        df_pass.position_x,
        df_pass.position_y,
        alpha=0.2,
        s=100,
        color="white",
        ax=ax,
    )


def plot_passnetwork(df, team=" "):
    """
    Plot a pass network for a given team, based on a DataFrame of events.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the events data.
    team : str
        Name of the team to plot the pass network for.

    Returns:
    --------
    None
    """
    # test for valid inputs
    if team == " ":
        raise ValueError("Please enter a team name")

    # create pitch to plot
    pitch = Pitch(
        pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b"
    )
    # fig, ax = pitch.draw(figsize=(10, 6))
    # maybe change pitch.grid to pitch.draw as previous function
    fig, ax = pitch.grid(
        grid_height=0.9,
        title_height=0.06,
        axis=False,
        endnote_height=0.04,
        title_space=0,
        endnote_space=0,
    )

    # first iteration of code remove observations after first substitution
    # second iteration should plot the players subbed on with new color/alpha
    team_chosen = team
    sub = (
        df[df["type"].isin(["Substitution"])]
        .loc[df["team"] == team_chosen]
        .iloc[0]["index"]
    )
    df_passnet = df[
        (df["type"].isin(["Pass"]))
        & (df["pass_type"].isin([np.nan, "Goal Kick"]))
        & (df["team"] == team_chosen)
        & (df["pass_outcome"].isin([np.nan]))
        & (df["index"] < sub)
    ]
    df_passnet[["position_x", "position_y"]] = pd.DataFrame(
        df_passnet.location.tolist(), index=df_passnet.index
    )
    df_passnet[["end_pass_x", "end_pass_y"]] = pd.DataFrame(
        df_passnet.pass_end_location.tolist(), index=df_passnet.index
    )
    # create temporary scatterf_df and lines_df to plot the vertices and edges
    # TODO: make sure the method using enumerate is the best way to do this
    scatter_df = pd.DataFrame()
    for i, name in enumerate(df_passnet["player"].unique()):
        passx = df_passnet.loc[df_passnet["player"] == name][
            "position_x"
        ].to_numpy()
        recx = df_passnet.loc[df_passnet["pass_recipient"] == name][
            "end_pass_x"
        ].to_numpy()
        passy = df_passnet.loc[df_passnet["player"] == name][
            "position_y"
        ].to_numpy()
        recy = df_passnet.loc[df_passnet["pass_recipient"] == name][
            "end_pass_y"
        ].to_numpy()
        scatter_df.at[i, "player"] = name
        # make sure that x and y location for each circle representing the
        # player is the average of passes and receptions
        scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
        scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
        # calculate number of passes
        scatter_df.at[i, "no"] = df_passnet.loc[df_passnet["player"] == name][
            "type"
        ].count()

    # adjust the size of a circle so that the player who made more passes
    scatter_df["marker_size"] = (
        scatter_df["no"] / scatter_df["no"].max() * 1500
    )

    # counting passes between players
    df_passnet["pair_key"] = df_passnet.apply(
        lambda x: "_".join(sorted([x["player"], x["pass_recipient"]])), axis=1
    )
    lines_df = (
        df_passnet.groupby(["pair_key"]).position_x.count().reset_index()
    )
    lines_df.rename({"position_x": "pass_count"}, axis="columns", inplace=True)
    # setting a treshold. try to investigate how it changes when you change it.
    lines_df = lines_df[lines_df["pass_count"] > 2]

    # plot the average position of players
    pitch.scatter(
        scatter_df.x,
        scatter_df.y,
        s=scatter_df.marker_size,
        color="#f99f84",
        edgecolors="white",
        linewidth=1,
        alpha=1,
        ax=ax["pitch"],
        zorder=3,
    )
    for i, row in scatter_df.iterrows():
        pitch.annotate(
            row.player,
            xy=(row.x, row.y),
            c="white",
            va="center",
            ha="center",
            weight="bold",
            size=12,
            ax=ax["pitch"],
            zorder=4,
        )

    # plot the connections between players
    # TODO: make sure the method using iterrows is the best way to do this
    for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row["pair_key"].split("_")[1]
        # take the average location of players to plot a line between them
        player1_x = scatter_df.loc[scatter_df["player"] == player1]["x"].iloc[
            0
        ]
        player1_y = scatter_df.loc[scatter_df["player"] == player1]["y"].iloc[
            0
        ]
        player2_x = scatter_df.loc[scatter_df["player"] == player2]["x"].iloc[
            0
        ]
        player2_y = scatter_df.loc[scatter_df["player"] == player2]["y"].iloc[
            0
        ]
        num_passes = row["pass_count"]
        # adjust the line width so that the more passes, the wider the line
        line_width = num_passes / lines_df["pass_count"].max() * 10
        # plot lines on the pitch
        pitch.lines(
            player1_x,
            player1_y,
            player2_x,
            player2_y,
            alpha=1,
            lw=line_width,
            zorder=2,
            color="#f99f84",
            ax=ax["pitch"],
        )
