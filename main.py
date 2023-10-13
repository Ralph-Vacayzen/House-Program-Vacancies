import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='House Program Vacancies',
    page_icon='🏠'
)

st.caption('VACAYZEN')
st.title('House Program Vacancies')
st.info('A tool to determine which properties are vacant.')

option = st.selectbox('Which house program are you looking into?',['Golf Carts','Bikes'])


if option == 'Golf Carts':

    st.subheader('Required reports')

    st.write('Current Golf Cart Program')
    with st.expander(label='How to pull report'):
        st.write('[GART - Partner Program Register](https://docs.google.com/spreadsheets/d/1jm0PfzBh_2rJy7LnFvGyCr-KqOKaMdp8nCj4-vk8xrI/edit#gid=723755011)')
        st.video('https://youtu.be/W6Hl5DsI6Go')

    st.write('Occupancy')
    with st.expander(label='How to create report'):
        st.download_button('Download Occupancy Template', pd.read_csv('template.csv', index_col=False).to_csv(index=False),'template.csv',use_container_width=True)
        st.video('https://youtu.be/gpmI9IL6GDg')

    left, right = st.columns(2)
    file_gp = left.file_uploader('Partner Program Register (PPR) - GART.csv','csv')
    if file_gp is not None: gp = pd.read_csv(file_gp, index_col=False)

    file_oc = right.file_uploader('template.csv','csv')
    if file_oc is not None: oc = pd.read_csv(file_oc, index_col=False)

    if (file_gp is not None and file_oc is not None):
        st.divider()
        left, right = st.columns(2)
        option = left.selectbox('Partner',options=gp.PARTNER.unique())
        start = right.date_input('Date of Vacancy')
        start = pd.to_datetime(start)

        pp = gp[gp.PARTNER == option]
        oc = oc.drop_duplicates()

        pp.columns = ['geo','partner','unit','info','vendor_code','name','area','address','order','billing','quantity','type','storage','number','lock','plate','vin','waiver','start','end']

        pp = pp[['unit','name','area','address','order','quantity','type','storage','number','lock','plate','vin']]

        df = pd.merge(pp,oc,'left','unit')
        df.arrival = pd.to_datetime(df.arrival)
        df.departure = pd.to_datetime(df.departure)

        occupied = df[(df.arrival <= start) & (df.departure > start)]
        occupied = occupied.unit.unique()

        def IsUnitOccupied(unit):
            return unit in occupied
        
        df['occupied'] = df.unit.apply(IsUnitOccupied)
        df = df[~(df.occupied)]
        df['vacant_on'] = start
        df = df.rename(columns={'arrival':'next_arrival'})
        df['days_vacant'] = (df.next_arrival - df.vacant_on).dt.days
        df = df[df.days_vacant.isna() | (df.days_vacant > 0)]
        df.days_vacant = df.days_vacant.fillna(30)
        df = df.sort_values(by=['unit','next_arrival'])
        df = df.drop_duplicates(subset='unit',keep='first')

        df = df[['unit','vacant_on','next_arrival','days_vacant','area','address','quantity','type']]
        

        st.write(df)
        st.download_button('Download Results',df.to_csv(index=False),'vacant.csv',use_container_width=True)


if option == 'Bikes':

    st.subheader('Required reports')

    st.write('Current Bike Program')
    with st.expander(label='How to pull report'):
        st.write('[GART - Partner Program Register](https://docs.google.com/spreadsheets/d/1jm0PfzBh_2rJy7LnFvGyCr-KqOKaMdp8nCj4-vk8xrI/edit#gid=723755011)')
        st.video('https://youtu.be/W6Hl5DsI6Go')

    st.write('Occupancy')
    with st.expander(label='How to create report'):
        st.download_button('Download Occupancy Template', pd.read_csv('template.csv', index_col=False).to_csv(index=False),'template.csv',use_container_width=True)
        st.video('https://youtu.be/gpmI9IL6GDg')

    left, right = st.columns(2)
    file_bp = left.file_uploader('Partner Program Register (PPR) - BIKE.csv','csv')
    if file_bp is not None: gp = pd.read_csv(file_bp, index_col=False)

    file_oc = right.file_uploader('template.csv','csv')
    if file_oc is not None: oc = pd.read_csv(file_oc, index_col=False)

    if (file_bp is not None and file_oc is not None):
        st.divider()
        left, right = st.columns(2)
        option = left.selectbox('Partner',options=gp.PARTNER.unique())
        start = right.date_input('Date of Vacancy')
        start = pd.to_datetime(start)

        pp = gp[gp.PARTNER == option]
        oc = oc.drop_duplicates()

        pp.columns = ['geo','partner','unit','info','vendor_code','name','area','address','order','billing','quantity','type','lock','storage','start','end']

        pp = pp[['unit','name','area','address','order','quantity','type','lock','storage']]

        df = pd.merge(pp,oc,'left','unit')
        df.arrival = pd.to_datetime(df.arrival)
        df.departure = pd.to_datetime(df.departure)

        occupied = df[(df.arrival <= start) & (df.departure > start)]
        occupied = occupied.unit.unique()

        def IsUnitOccupied(unit):
            return unit in occupied
        
        df['occupied'] = df.unit.apply(IsUnitOccupied)
        df = df[~(df.occupied)]
        df['vacant_on'] = start
        df = df.rename(columns={'arrival':'next_arrival'})
        df['days_vacant'] = (df.next_arrival - df.vacant_on).dt.days
        df = df[df.days_vacant.isna() | (df.days_vacant > 0)]
        df.days_vacant = df.days_vacant.fillna(30)
        df = df.sort_values(by=['unit','next_arrival'])
        df = df.drop_duplicates(subset='unit',keep='first')

        df = df[['unit','vacant_on','next_arrival','days_vacant','area','address','quantity','type']]
        

        st.write(df)
        st.download_button('Download Results',df.to_csv(index=False),'vacant.csv',use_container_width=True)