#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("679043b4-298f-4b7f-9394-54d64db46007")


# In[2]:


import time
my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)


# In[7]:


st.title('Near Megadashboard')
st.write('')
st.markdown('**Near Protocol** Near Protocol is a decentralized application (DApp) platform that focuses on usability among developers and users. As a competitor of Ethereum, NearProtocol is also smart-contract capable and a proof-of-stake (PoS) blockchain. It uses sharding technology to achieve scalability, a core aspect discussed later. The native token, NEAR, is used for transaction fees and storage on the Near crypto platform. Tokens can also be used for staking by NEAR tokenholders who wish to become transaction validators and help achieve network consensus.')
st.markdown('Near was built by the NeaCollective and conceptualized as a community-run cloud computing platform designed to host decentralized applications. It was also built to be both developer and user-friendly, hence having features such as account names that are human-readable (instead of cryptographic wallet addresses).')
st.markdown('**How does Near Protocol work?** Decentralized applications have boomed in the crypto community, with DApps that run the gamut from games to financial services. However, it has also become apparent that scalability remains a problem in most blockchains.')
st.markdown('The issue of scalability is common among blockchains, especially among older ones such as Bitcoin and Ethereum. The challenges are mainly brought about by blockchains difficulty in handling large numbers of transactions at fast speeds and manageable costs.')
st.markdown('The intention of this analysis is to take a look at the following main aspects of **Near Protocol**:')
st.markdown('1. Activity')
st.markdown('2. Staking')
st.markdown('3. Development')
st.markdown('4. Supply')
st.write('')
st.subheader('1. Activity on Near')
st.markdown('**Methods:**')
st.write('In this analysis we will focus on Near activity. More specifically, we will analyze the following data:')
st.markdown('● Daily number of NFT sales.')
st.markdown('● Daily amount of sellers and buyers.')
st.markdown('● Daily NFT sales volume (Near)')
st.markdown('● Min, max and average NFT price.')
st.write('')

sql="""
with 
t1 as (
SELECT
trunc(x.block_timestamp,'day') as date,
count(distinct x.tx_hash) as transactions,
count(distinct x.tx_signer) as active_users,
transactions/active_users as avg_tx_per_user,
sum(transaction_fee/pow(10,24)) as fees,
avg(transaction_fee/pow(10,24)) as avg_tx_fee
  from near.core.fact_transactions x
  where x.block_timestamp>=current_date-INTERVAL '3 MONTHS'
  group by 1
  ),
  t2 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_hash) as swaps,
count(distinct trader) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from near.core.ez_dex_swaps y
  where y.block_timestamp>=current_date-INTERVAL '3 MONTHS'
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as nft_sales,
count(distinct z.tx_signer) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from near.core.ez_nft_mints z
  where z.block_timestamp>=current_date-INTERVAL '3 MONTHS'
  group by 1
  )
  SELECT
  t1.date, transactions,active_users,avg_tx_per_user,fees,avg_tx_fee,swaps,swappers,avg_swaps_per_swapper,
  nft_sales,nft_buyers,nft_bought_per_user
  from t1,t2,t3 where t1.date=t2.date and t1.date=t3.date
order by 1 asc 

"""

st.experimental_memo(ttl=50000)
def memory(code):
    data=sdk.query(code)
    return data

results = memory(sql)
df = pd.DataFrame(results.records)
df.info()

with st.expander("Check the analysis"):
    base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='darkred').encode(y=alt.Y('active_users:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='red',opacity=0.5).encode(y='transactions:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily transactions and active users',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='date:N', y='avg_tx_per_user:Q')
        .properties(title='Daily average transactions per user',width=600))

    base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='darkblue').encode(y=alt.Y('avg_tx_fee:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='blue',opacity=0.5).encode(y='fees:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily fees and average transaction fee',width=600))

    base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='darkgreen').encode(y=alt.Y('swappers:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='green',opacity=0.5).encode(y='swaps:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily swaps and swappers',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='date:N', y='avg_swaps_per_swapper:Q')
        .properties(title='Daily average swaps per user',width=600))

    base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='black').encode(y=alt.Y('nft_buyers:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='yellow',opacity=0.5).encode(y='nft_sales:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily NFT sales and purchasers',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='date:N', y='nft_bought_per_user:Q')
        .properties(title='Daily NFT buys per user',width=600))




# In[8]:


st.subheader("2. Staking")
st.markdown('**Methods:**')
st.write('In this analysis we will focus on Near staking. More specifically, we will analyze the following data:')
st.markdown('● Percentage of Near staked')
st.markdown('● Total near staked and number of validators')
st.markdown('● Nakamoto coefficient')
st.markdown('● Top validators percentage share')


with st.expander("Check the analysis"):

    sql="""
    WITH
    staking as (
    SELECT tx_hash
    FROM near.core.fact_actions_events_function_call
    WHERE method_name in ('deposit_and_stake','stake','stake_all') and block_timestamp>=current_date-INTERVAL '3 MONTHS'
    ), stakes as (
    SELECT
    block_timestamp, tx_hash as tx, tx_receiver as validator, tx_signer as delegator,
    tx:actions[0]:FunctionCall:deposit/pow(10,24) near_staked
    FROM near.core.fact_transactions
    WHERE tx_hash in (select * from staking) and block_timestamp>=current_date-INTERVAL '3 MONTHS'
    ),
    monthly as (
    SELECT
    trunc(block_timestamp,'week') as months, tx, validator, near_staked
    FROM stakes WHERE near_staked is not null
    ),
    totals as (
    SELECT
    months, sum(near_staked) as month_near_staked, sum(month_near_staked) over (order
    by months)as total_near_staked
    from monthly
    group by 1 order by 1
    ),
    ranking as (
    SELECT
    months, validator, count(distinct tx) as txs, sum(near_staked) as total_near_delegated,
    sum(total_near_delegated) over (partition by validator order by months) as cumulative_near_delegated
    FROM monthly
    group by 1,2
    )
    select
    x.months, total_near_staked,
    count(distinct validator) as n_validators
    from totals x
    join ranking y on x.months=y.months
    group by 1,2
    order by 1 asc
    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()


    base=alt.Chart(df).encode(x=alt.X('months:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='darkred').encode(y=alt.Y('total_near_staked:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='red',opacity=0.5).encode(y='n_validators:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Weekly validators and NEAR staked',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='n_validators:N', y='total_near_staked:Q')
        .properties(title='NEAR staked per number of validators',width=600))

    sql="""
    WITH
    transactions as (
    SELECT tx_hash
    FROM near.core.fact_actions_events_function_call
    WHERE method_name IN ('deposit_and_stake')
    ),
    stakes as (
    SELECT
    block_timestamp, tx_hash as tx, tx_receiver as validator, tx_signer as user,
    tx:actions[0]:FunctionCall:deposit/pow(10,24) near_staked
    FROM near.core.fact_transactions
    WHERE tx_hash in (select * from transactions)
    ),
    monthly as (
    SELECT
    trunc(block_timestamp,'week') as months, tx, validator, near_staked
    FROM stakes WHERE near_staked is not null
    ),
    totals as (
    SELECT
    months, sum(near_staked) as month_near_staked, sum(month_near_staked) over
    (order by months)as total_near_staked
    from monthly
    group by 1 order by 1
    ),
    ranking as (
    SELECT
    months, validator, count(distinct tx) as txs, sum(near_staked) as
    total_near_delegated, sum(total_near_delegated) over (partition by validator order
    by months) as cumulative_near_delegated
    FROM monthly
    group by 1,2
    ),
    stats as (
    SELECT
    months,
    50 as bizantine_fault_tolerance, total_near_staked,
    (total_near_staked*bizantine_fault_tolerance)/100 as threshold--,
    from totals
    ),
    stats2 as (
    select *,
    1 as numbering, sum(numbering) over (partition by months order by
    cumulative_near_delegated desc) as rank
    from ranking
    ),
    stats3 as (
    SELECT
    months, validator, cumulative_near_delegated, rank,
    sum(cumulative_near_delegated) over (partition by months order by rank asc) as
    total_staked
    from stats2
    order by rank asc)
    SELECT
    a.months, validator, count(case when total_staked <= threshold then 1 end) as
    nakamoto_coeff
    from stats3 a
    join stats b
    on a.months = b.months
    and a.months>=current_date-INTERVAL '3 MONTHS'
    group by 1,2
    order by 1 asc
    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()


    st.altair_chart(alt.Chart(df)
        .mark_bar()
        .encode(x='months:N', y='nakamoto_coeff:Q')
        .properties(title='Weekly Near Protocol Nakamoto Coefficient',width=600))


# In[19]:


st.subheader("3. Development")
st.markdown('**Methods:**')
st.write('In this analysis we will focus on Near development. More specifically, we will analyze the following information:')
st.markdown('● New deployed contracts')
st.markdown('● Top new contracts by transactions')
st.markdown('● Top new contracts by weekly transactions')
st.markdown('● Top new contracts by average transactions fee')
st.markdown('● Top new contracts by total and average transactions fee')
st.markdown('● Top 10 contracts by gas spent')


sql="""
SELECT
trunc(first_date,'day') as date,
count(distinct receiver_id ) as new_contracts,
sum(new_contracts) over (order by date) as cum_new_contracts
from (select
receiver_id,
min(x.block_timestamp) as first_date
from near.core.fact_actions_events x
join near.core.fact_receipts y on x.tx_hash=y.tx_hash
where action_name = 'DeployContract'
group by 1) where first_date >= CURRENT_DATE - INTERVAL '3 MONTHS'
group by 1
order by 1 asc

"""

results = memory(sql)
df = pd.DataFrame(results.records)
df.info()

with st.expander("Check the analysis"):

    base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_line(color='darkblue').encode(y=alt.Y('new_contracts:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='blue',opacity=0.5).encode(y='cum_new_contracts:Q')
    st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Near new deployed contracts',width=600))


    sql="""
    with tab1 as (
    select
    tx_hash, block_timestamp
    from near.core.fact_actions_events
    where action_name = 'DeployContract'
    ),
    tab2 as (
    select
    x.tx_hash as transactions, x.block_timestamp as time
    from near.core.fact_actions_events_function_call x
    join tab1 y
    on (x.tx_hash = y.tx_hash
    and x.block_timestamp = y.block_timestamp)
    where method_name = 'new'
    ),
    tab3 as (
    select
    tx.tx_receiver, tx.block_timestamp
    from near.core.fact_transactions tx
    join tab2 y
    on tx.tx_hash = y.transactions
    and tx.block_timestamp = y.time
    ),
    tab4 as (
    select
    tx_receiver, block_timestamp, row_number() over(partition by tx_receiver
    order by block_timestamp) as row_num
    from tab3
    ),
    tab5 as (
    select *
    from tab4
    where row_num = 1
    )
    select
    case when tx.tx_receiver
    ='5238a70e554c4b1b3d75606fce1b9bb2efe96513dc0713d4774edf2a9b15db14' then 'other'
    else tx.tx_receiver end as tx_receiver,
    count(distinct tx.tx_hash) as number_of_tx
    from near.core.fact_transactions tx
    join tab5 contract
    on tx.tx_receiver = contract.tx_receiver and tx.block_timestamp >=
    contract.block_timestamp
    where contract.block_timestamp::date >= CURRENT_DATE - 90
    group by 1
    order by number_of_tx desc limit 10
    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()

    st.altair_chart(alt.Chart(df)
        .mark_bar()
        .encode(x='tx_receiver:N', y='number_of_tx:Q',color=alt.Color('number_of_tx', scale=alt.Scale(scheme='dark2')))
        .properties(title='Top contracts by transactions executed',width=600))


    sql="""
    with tab1 as (
    select
    tx_hash, block_timestamp
    from near.core.fact_actions_events
    where action_name = 'DeployContract'
    ),
    tab2 as (
    select
    x.tx_hash as transactions, x.block_timestamp as time
    from near.core.fact_actions_events_function_call x
    join tab1 y
    on (x.tx_hash = y.tx_hash
    and x.block_timestamp = y.block_timestamp)
    where method_name = 'new'
    ),
    tab3 as (
    select
    tx.tx_receiver, tx.block_timestamp
    from near.core.fact_transactions tx
    join tab2 y
    on tx.tx_hash = y.transactions
    and tx.block_timestamp = y.time
    ),
    tab4 as (
    select
    tx_receiver, block_timestamp, row_number() over(partition by tx_receiver
    order by block_timestamp) as row_num
    from tab3
    ),
    tab5 as (
    select *
    from tab4
    where row_num = 1
    ),
    tab6 as (
    select
    tx.tx_receiver, count(distinct tx.tx_hash) as number_of_tx
    from near.core.fact_transactions tx
    join tab5 contract
    on tx.tx_receiver = contract.tx_receiver and tx.block_timestamp >=
    contract.block_timestamp
    where contract.block_timestamp::date >= CURRENT_DATE - 90
    group by 1
    order by number_of_tx desc limit 10
    )
    select
    trunc (block_timestamp,'week') time,
    case when tx_receiver
    ='5238a70e554c4b1b3d75606fce1b9bb2efe96513dc0713d4774edf2a9b15db14' then 'other'
    else tx_receiver end as tx_receiver,
    avg(transaction_fee/pow(10,24)) as avg_tx_fee
    from near.core.fact_transactions
    where block_timestamp::date >= CURRENT_DATE - 90
    and tx_receiver in (select tx_receiver from tab6)
    group by 1,2
    order by 1

    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='time:N', y='avg_tx_fee:Q',color=alt.Color('tx_receiver', scale=alt.Scale(scheme='Dark2')))
        .properties(title='Average transaction fee over time per contract',width=600))

    sql="""
    select
    distinct tx_receiver,
    sum(gas_used)/pow(10,12) as total_gas
    from near.core.fact_transactions
    group by 1 order by 2 desc
    limit 10
    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()

    st.altair_chart(alt.Chart(df)
        .mark_bar()
        .encode(x='tx_receiver:N', y='total_gas:Q',color=alt.Color('total_gas', scale=alt.Scale(scheme='dark2')))
        .properties(title='Top 10 contracts by gas spent',width=600))


# In[21]:


st.subheader("4. Supply")
st.markdown('**Methods:**')
st.write('In this analysis we will focus on NEAR transfers and NEAR wallets supply. More specifically, we will analyze the following data:')
st.markdown('● NEAR transfers')
st.markdown('● NEAR volume transferred')
st.markdown('● Active users transferring')
st.markdown('● Supply in NEAR wallets')

sql="""
SELECT
trunc(block_timestamp,'day') as date,
sum(deposit/pow(10,24)) as volume,
count(distinct tx_signer) as users,
count(distinct tx_hash) as transfers
from near.core.fact_transfers
group by 1
order by 1 asc 
"""

results = memory(sql)
df = pd.DataFrame(results.records)
df.info()

with st.expander("Check the analysis"):

    st.altair_chart(alt.Chart(df)
        .mark_bar()
        .encode(x='date:N', y='transfers:Q')
        .properties(title='Daily transfers',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_line()
        .encode(x='date:N', y='users:Q')
        .properties(title='Daily users transferring',width=600))

    st.altair_chart(alt.Chart(df)
        .mark_area()
        .encode(x='date:N', y='volume:Q')
        .properties(title='Daily volume transferred',width=600))


    sql="""
    with
      ins as (
    SELECT distinct tx_signer,
    sum(deposit/pow(10,24)) as total_sent
      from near.core.fact_transfers
      group by 1
      ),
    outs as (
      SELECT distinct tx_receiver,
    sum(deposit/pow(10,24)) as total_received
      from near.core.fact_transfers
      group by 1
    )
    SELECT
    ifnull(tx_receiver,tx_signer) as user,
    ifnull(total_received,0) as volume_received,
    ifnull(total_sent,0) as volume_sent,
    volume_received-volume_sent as current_supply
    from ins
    full join outs on ins.tx_signer=outs.tx_receiver
    order by 4 desc limit 10

    """

    results = memory(sql)
    df = pd.DataFrame(results.records)
    df.info()

    base=alt.Chart(df).encode(x=alt.X('user:O', axis=alt.Axis(labelAngle=325)))
    line=base.mark_bar(color='red').encode(y=alt.Y('volume_sent:Q', axis=alt.Axis(grid=True)))
    bar=base.mark_bar(color='green').encode(y='volume_received:Q')
    st.altair_chart((bar + line).properties(title='Amount in and out per wallet',width=600))


    st.altair_chart(alt.Chart(df)
        .mark_bar()
        .encode(x='user:N', y='current_supply:Q',color=alt.Color('current_supply', scale=alt.Scale(scheme='dark2')))
        .properties(title='Current supply of each NEAR wallet',width=600))


# In[22]:


st.markdown('This dashboard has been done by _Cristina Tintó_ powered by **Flipside Crypto** data and carried out for **MetricsDAO**.')


# In[ ]:




