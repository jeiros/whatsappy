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

def plot_hour_per_user(df):
    new_df = df.groupby([df.index.hour, 'sender']).count()
    ax = new_df.unstack()['message'].plot(kind='bar',
        figsize=(10, 8), stacked=True, colormap='Paired'
    )
    ax.set_xlabel('hour')
    return ax