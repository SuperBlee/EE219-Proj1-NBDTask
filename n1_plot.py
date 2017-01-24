"""
Code of Project-1 Network Backup Dataset
EE219 2017 Winter
Task 1: Plot the distribution of sum of data backup every 21 days

Zeyu Li
Jan 21, 2017

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tools



def transform_weekday(data_frame, weekday_column_name, new_column_name):
    """
    Transform the weekday words to numbers, 'Monday' to 1, 'Tuesday' to 2, etc.
    And append the new column to the existed data frame
    :param data_frame: input data frame
    :param weekday_column_name: the column name containing weekday words
    :param new_column_name: the new generated column appending to the existed frame
    :return: the new data frame with appended column
    """
    weekday_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_to_num_dict = {weekday_n: i+1 for i, weekday_n in enumerate(weekday_name)}
    column_of_weekday_word = data_frame.ix[:, weekday_column_name]
    new_column = column_of_weekday_word.apply(lambda x: weekday_to_num_dict[x])
    data_frame[new_column_name] = new_column
    return data_frame


def calculate_num_day(data_frame, new_column_name, week_num_column_name, weekday_num_column_name):
    """
    Appending another column with number of days computed by:
        num_of_days = 7 * (week_num_column_name - 1) + weekday_num_column_name
    :param data_frame: Data frame to compute on.
    :param new_column_name: The new data column.
    :param week_num_column_name: ...
    :param weekday_num_column_name: ...
    :param period_num: a number derived by num_of_days / 21
    :param period: Time period length, 20 or 21
    :return: The appended new data frame
    """
    new_column = 7 * (data_frame.ix[:, week_num_column_name] - 1) + data_frame.ix[:, weekday_num_column_name]
    data_frame[new_column_name] = new_column
    return data_frame


if __name__ == '__main__':
    input_file_name = 'network_backup_dataset.csv'
    original_data = tools.read_data(input_file_name)
    data = transform_weekday(original_data, 'Day of Week', 'Number of Weekday')
    data = calculate_num_day(data, 'Num of the day', 'Week #', 'Number of Weekday')

    # Group the data by 'Week #', 'Number of Weekday' and take the sum of "Size of Backup (GB)"
    grouped_data = data.groupby(['Week #', 'Work-Flow-ID', 'Number of Weekday'])['Size of Backup (GB)'].sum()
    # print grouped_data
    listed_data = list(grouped_data)
    print grouped_data
    # print listed_data
    # print len(listed_data)

    # The listed data has len of 525
    # 15 Weeks * 5 Workflows * 7 Days/Week
    # sep_listed_data = [listed_data[x:x+21] for x in range(0, len(listed_data), 21)]

    # Divided by 3 weeks, should be 5 period
    by_three_weeks = [listed_data[i:i+105] for i in range(0, len(listed_data), 105)]

    period_list = []
    # Divide by weeks and workflows, should be 25 sets
    for period in by_three_weeks:
        # workflow list over weekdays
        list_all_wf = []
        for wf in range(0, 5):
            list_wf = []
            for week in range(0,3):
                base = week*35 + wf*7
                list_wf_week = period[base:base+7]
                list_wf += list_wf_week
            list_all_wf.append(list_wf)
        period_list.append(list_all_wf)


    # for i in range(0,len(period_list)):
    #     for j in range(0,5):
    #         print period_list[i][j]
    #         print len(period_list[i][j])


    # Start to plot
    x_days = np.arange(1,22)
    fig = plt.figure(figsize=(30,20))

    for i in period_list:
        for j in i:
            print len(j)
    for i in range(0,len(period_list)):
        sub_fig = fig.add_subplot(2,3, i+1)
        # for j in range(0,5):
            # y_data = np.array(period_list[i][j])
        # y_data = period_list[i][3]
        sub_fig.plot(x_days, period_list[i][1], '-',
                     x_days, period_list[i][2], '-',
                     x_days, period_list[i][3], '-',
                     x_days, period_list[i][0], '-',
                     x_days, period_list[i][4], '-')
        sub_fig.set_xticks(x_days)
        sub_fig.set_title("Data of {}-th Week".format(i))
        sub_fig.set_xlabel("# of Days")
        sub_fig.set_ylabel("Sum of Size of Backup (GB)")
        sub_fig.set_xlim([0.5, 21.5])
        sub_fig.set_ylim([0, 13])
    fig.savefig('NBD_Task1.png')




     # for i in range(0, len(sep_listed_data)):
    #     fig_list.append(fig.add_subplot(2, 3, i+1))
    #     fig_list[i].plot(x_days, sep_listed_data[i], '-')
    #     print sep_listed_data[i]
    #     fig_list[i].set_xticks(x_days)
    #     fig_list[i].set_title("Data of {}-th Week".format(i))
    #     fig_list[i].set_xlabel("# of Days")
    #     fig_list[i].set_ylabel("Sum of Size of Backup (GB)")
    #     fig_list[i].set_xlim([1, 21])
    #     fig_list[i].set_ylim([5, 20])
    # fig.savefig('NBD_Task1.png')
