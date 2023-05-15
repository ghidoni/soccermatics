import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import pandas as pd
import numpy as np


def plot_shots_df(df):
    # create pitch to plot
    pitch = Pitch(pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b")
    fig, ax = pitch.draw(figsize=(8, 5))
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
        marker_size_xg = shot["shot_statsbomb_xg"]
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
            xg_circle = plt.Circle((x, y), marker_size_xg, color="white")
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
            xg_circle = plt.Circle((120 - x, 80 - y), marker_size_xg, color="white")
        ax.add_patch(shot_circle)
        # ax.add_patch(xg_circle)


def plot_passes_arrow(df, team=" ", player=" "):
    # test for valid inputs
    if team == " " and player == " ":
        raise ValueError("Please enter either team or player name")
    elif team != " " and player != " ":
        raise ValueError("Please enter only team or player name")
    # create pitch to plot
    pitch = Pitch(pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b")
    fig, ax = pitch.draw(figsize=(10, 6))
    # create df_pass
    df_pass = df[
        (df["type"].isin(["Pass"])) & (df["pass_type"].isin([np.nan, "Goal Kick"]))
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
        df_pass.position_x, df_pass.position_y, alpha=0.2, s=100, color="white", ax=ax
    )


def plot_passnetwork(df, team=" "):
    # test for valid inputs
    if team == " ":
        raise ValueError("Please enter a team name")

    # create pitch to plot
    pitch = Pitch(pitch_type="statsbomb", line_color="grey", pitch_color="#1b1b1b")
    fig, ax = pitch.draw(figsize=(10, 6))

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
