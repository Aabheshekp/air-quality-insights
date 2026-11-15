from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Air Quality Insights", page_icon="🌿", layout="wide")
st.title("Air Quality Insights")
st.caption("Compare pollutant levels and daily AQI patterns across sample cities.")
df=pd.read_csv(Path(__file__).parent/"data"/"air_quality.csv",parse_dates=["date"])
cities=st.sidebar.multiselect("Cities",sorted(df.city.unique()),default=sorted(df.city.unique()))
pollutant=st.sidebar.selectbox("Pollutant",["aqi","pm25","pm10","no2"])
f=df[df.city.isin(cities)]
if f.empty: st.warning("Choose at least one city."); st.stop()
a,b,c=st.columns(3)
a.metric("Cities",f.city.nunique())
b.metric("Average AQI",f.aqi.mean().round(1))
c.metric("Days above AQI 100",int(f.aqi.gt(100).sum()))
st.subheader(f"{pollutant.upper()} over time")
wide=f.pivot_table(index="date",columns="city",values=pollutant,aggfunc="mean").sort_index()
st.line_chart(wide)
left,right=st.columns(2)
with left: st.subheader("Average AQI by city"); st.bar_chart(f.groupby("city").aqi.mean().sort_values())
with right: st.subheader("AQI category counts"); f2=f.assign(category=pd.cut(f.aqi,[-1,50,100,150,200,300,1000],labels=["Good","Moderate","Sensitive","Unhealthy","Very unhealthy","Hazardous"])); st.bar_chart(f2.groupby(["city","category"],observed=False).size().unstack(fill_value=0))
st.dataframe(f.sort_values("date",ascending=False),use_container_width=True,hide_index=True)
st.download_button("Download selected rows",f.to_csv(index=False),"air-quality.csv","text/csv")
st.caption("Demo values are illustrative and are not official measurements or health guidance.")
