from matplotlib import pyplot as plt
from .parse import count_user_messages


def plot_messages_per_user(df):
    """
    Plot the total messages by each user in descending order
    :param user_messages_series:
    :return:
    """
    user_messages_series = count_user_messages(df)
    ax = user_messages_series.sort_values(ascending=False).plot(kind="bar")
    ax.set_ylabel('Messages')
    ax.set_xlabel('')
    return ax
