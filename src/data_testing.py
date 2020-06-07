# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# a cell for importing modules and setting constants:

import matplotlib.pyplot as plt
import numpy as np
from get_cursor import get_cursor
import statements


# Our time range, in days:
MIN_ = -31
MAX_ = 31

# get interface to sqlite database, column names
curs, db = get_cursor('../me.db')
info = [curs.execute('pragma table_info(Daily_Functionality);').fetchall()][0]
labels = [x[1] for x in info]
# column_labels is a dictionary 
# in which values are lists of 420+ 2-string tuples:
# column_labels[key] = [ 420*(<date_string>, <number_string>) ]
# for each key
column_labels = {}
for a in labels:
    column_labels[a] = curs.execute('select Date, ' + a + ' from Daily_Functionality;').fetchall()

# master_keys is a dictionary with string keys that refer either to lists of other strings or None
# master_keys's keys are sigma column names, the values they refer to are their subordinate column names
master_keys = {}
master_keys[statements.keys[3]] = [statements.keys[0], statements.keys[1], statements.keys[2]] 
master_keys[statements.keys[7]] = [statements.keys[4], statements.keys[5], statements.keys[6]]
master_keys[statements.keys[8]] = None
master_keys[statements.keys[11]] = [statements.keys[9], statements.keys[10]]
master_keys[statements.keys[16]] = [statements.keys[12], statements.keys[13], statements.keys[14]]
master_keys[statements.keys[17]] = None
master_keys[statements.keys[18]] = None


# %%
# a cell for manually testing/running functions, 
# to be commented out the first time through defining functions:
pass
#print(np.array([x[1] for x in column_labels['Total_Work']][30:]))


# %%
# Section on fourier transformations to find out what my "cycle" really is using fourier transformations
# I have no real idea what to do with the value np.fft.fft() returns
def cycle(column_labels):
    for k in column_labels.keys():
        l = [v[1] for v in column_labels[k]]
        print(np.fft.fft(l))


# %%
def column_variability():
    # Information regarding the variability of each column in this cell:
    dates = [d[0] for d in column_labels['Date']]
    for k in column_labels.keys():
        temp_cols = []
        for m in range(len(column_labels[k])):
            try:
                temp_cols.append(float(column_labels[k][m][1]))
            except (TypeError, ValueError):
                pass
        #
        try:
            assert type(temp_cols[1]) == float
        except (AssertionError, IndexError):
            continue
        r = np.array(temp_cols)
        print(k + ': ')
        #fig = plt.figure()
        #ax = fig.add_axes([0, 0, len(dates)/40, 4])
        # a bar chart seems appropriate here...
        # bars for each column with variance and std. deviation as values
        # having a comparison chart for averages seems pointless here.
        print('\tAverage:', str(np.average(r)))
        print('\tVariance:', str(r.var()))
        print('\tStandard deviation:', str(r.std()))
        #
        column_labels[k] = r


# %%
def corr_over_time(labels, MIN_, MAX_):
    # Build list of factors to find relationships for
    # to find how factor affects cofactor up to 31 days in the future
    # and how it is affected by cofactor up to 31 days in the past
    factors = labels[9:20]
    factors.append(labels[5])
    relationships = {}
    for factor in factors:
        # a dictionary of dictionaries
        relationships[factor] = {}
        for cofactor in column_labels.keys():
            if cofactor not in [factor, 'Over_Extending', 'Notes', 'Date', 'Weekday']:
                # with each sub-dictionary referring to a list of correlation coefficients
                relationships[factor][cofactor] = []
                for time_delta in range(MIN_, MAX_+1):
                    x = np.array([])
                    index = 0
                    temp = []
                    try:
                        # for every day of distance we shorten the length data we use
                        # from the cofactor's column:
                        for c in range(len(column_labels[cofactor])-abs(time_delta)):
                            if time_delta < 0:
                                # day is negative, last $day number of cofactor values are excluded
                                # because $factor is dependent variable
                                temp.append(column_labels[cofactor][index])
                            else:
                                # day is positive, first $day number of cofactor values are excluded
                                # because $cofactor is dependent variable
                                temp.append(column_labels[cofactor][index+time_delta])
                            index += 1
                    except IndexError as e:
                        print(e)
                    # arrays are faster than lists
                    print('temp:', temp)
                    vals = np.array(temp)
                    print('vals:', vals)
                    if time_delta <= 0:
                        # we take the first $day number of values off of factor's column
                        print(
                            'len(vals):',
                            len(vals),
                            "\nnp.array([x[1] for x in column_labels['Total_Work']][abs(time_delta):]):",
                            np.array([x[1] for x in column_labels['Total_Work']][abs(time_delta):]),
                            '\nvals:',
                            vals,
                            sep='\n'
                        )
                        correlation = np.corrcoef(np.array([x[1] for x in column_labels['Total_Work']][abs(time_delta):]), vals)[0][1]
                    else:
                        # we take the last $day number of values off of factor's column
                        print(
                            'len(vals):',
                            len(vals),
                            "\nnp.array([x[1] for x in column_labels['Total_Work']][:-abs(time_delta)]):",
                            np.array([x[1] for x in column_labels['Total_Work']][:-abs(time_delta)]),
                            '\nvals:',
                            vals,
                            sep='\n'
                        )
                        correlation = np.corrcoef(np.array([x[1] for x in column_labels['Total_Work']][:-time_delta]), vals)[0][1]
                    relationships[factor][cofactor].append(correlation)
    # this is what we came for:
    return relationships


# %%
#for factor in relationships.keys():
#    for cofactor in relationships[factor].keys():
#        already_titled = False
#        index = 0
#        for value in relationships[factor][cofactor]:
#            if value > .2 and value < .3:
#                if not already_titled:
#                    print('factor:', factor)
#                    print('cofactor:', cofactor)
#                    already_titled = True
#                print('index, value:', str(index), value)
#            index += 1


# %%
def cross_relationships1(relationships):
    for factor in relationships.keys():
        num = 0
        for cofactor in relationships[factor]:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, MAX_/5, 1])
            ax.set_title('Correlation Over Time')
            ax.set_xlabel('Days Between Cofactor ' + cofactor + ' and ' + factor)
            ax.set_ylabel('Correlation Coefficient * 100:')
            try:
                thyme = list(range(MIN_, MAX_+1))
                assert thyme == len(relationships[factor][cofactor])
            except AssertionError as e:
                print(e)
                print('thyme != len(relationships[factor][cofactor])')
                print('len(thyme):', len(thyme))
                print('len(relationships[factor][cofactor]):', len(relationships[factor][cofactor]))
            values = [100*value for value in relationships[factor][cofactor]]
            ax.plot(thyme, relationships[factor][cofactor])
            plt.show()

def cross_relationships2():
    factor = 'Total_Vices'
    cofactor = 'Total_Work'
    fig = plt.figure()
    ax = fig.add_axes([0, 0, MAX_/5, 1])
    ax.set_title('Factor: Total_Vices; Cofactor: Total_Work')
    ax.set_xlabel('Days between Factor and Cofactor')
    ax.set_ylabel('Correlation Coefficient * 100')
    thyme = list(range(MIN_, MAX_+1))
    values = [100*value for value in relationships[factor][cofactor]]
    ax.plot(thyme, values)
    plt.show()


# %%
def close_(curs, db=None):
    # commit any transactions, close db connections:
    #db.commit()
    curs.close(); db.close()


if __name__ == '__main__':
    relationships = corr_over_time(labels, MIN_, MAX_)
    #cross_relationships1(relationships)
    close_(curs, db)