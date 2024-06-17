import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

  

def sidebar():

 #Panel for campain
  st.sidebar.header('Plot options')
  cmp_p = st.sidebar.radio('Choose a campain:', ['Campain 1','Campain 2','Campain 3','Campain 4','Campain 5','Last Campain',])
  
 #Panel for violin plot
  st.sidebar.subheader('Violin plot')
  vlncat_p = st.sidebar.radio('Choose one:', ['Complain','Education','Marrital','Kidhome', 'Teenhome'])
  vlnnum_p = st.sidebar.selectbox('Choose one:', 
  ['Age',  'Income',   'Recency',   'MntFruits',  'MntMeatProducts',  'MntSweetProducts',  'MntRegularProds',
  'NumDealsPurchases',  'NumWebPurchases',  'NumCatalogPurchases',  'NumStorePurchases',  'NumWebVisitsMonth',
  'MntTotal',  'Customer_Days'])

  #Panel for pairplot plot
  st.sidebar.subheader('Pairplot plot')
  pairplot_p  = st.sidebar.multiselect('Choose 4:', ['Income', 'Recency',  'MntFruits',  'MntMeatProducts',
  'MntSweetProducts',  'MntRegularProds',  'NumDealsPurchases',  'NumWebPurchases',  'NumCatalogPurchases',
  'NumStorePurchases',  'NumWebVisitsMonth',  'MntTotal',  'Customer_Days'])

  return cmp_p, vlncat_p, vlnnum_p, pairplot_p 

def choose_overall(overal_panel):
  if overal_panel == 'Campain 1':
    return 'AcceptedCmp1'
  if overal_panel == 'Campain 2':
    return 'AcceptedCmp2'
  if overal_panel == 'Campain 3':
    return 'AcceptedCmp3'
  if overal_panel == 'Campain 4':
    return 'AcceptedCmp4'
  if overal_panel == 'Campain 5':
    return 'AcceptedCmp5'
  if overal_panel == 'Last Campain':
    return 'Response'



def plot_bar(df):
  campaign_cols =['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5','Response']
  df_cmp = pd.DataFrame({})
  df_cmp[campaign_cols]=df[campaign_cols].replace({ "Accepted":1, "Not Accepted":0})  
  acceptance_percentages = df_cmp[campaign_cols].mean() * 100
  

  fig, ax = plt.subplots(figsize=(10, 6))
  ax.bar(acceptance_percentages.index, acceptance_percentages.values, color='skyblue')
  ax.set_xlabel('Campaigns')
  ax.set_ylabel('Percentage Accepted (%)')
  ax.set_title('Percentage of Customers Accepted Each Campaign')
  ax.set_ylim(0, 17.5)  # Ensure y-axis starts at 0 and goes up to 100
  ax.grid(True, axis='y')
  return fig

def plot_violin(df,campain,cat,val_cat):
  fig = go.Figure()
  fig.update_layout(
    autosize=False,
    width=500,
    height=300)
  fig.add_trace(go.Violin(x=df[cat][ df[campain] == val_cat[0] ],
                          y=df[num][ df[campain] == val_cat[0] ],
                          legendgroup='Accepted', scalegroup=val_cat[0], name=val_cat[0],
                          side='negative',
                          line_color='blue')
              )
  fig.add_trace(go.Violin(x=df[cat][ df[campain] == val_cat[1] ],
                          y=df[num][ df[campain] == val_cat[1] ],
                          legendgroup='Not Accepted', scalegroup=val_cat[1], name=val_cat[1],
                          side='positive',
                          line_color='orange')
              )
  fig.update_traces(meanline_visible=True)
  fig.update_layout(violingap=0, violinmode='overlay')
  return fig

df = pd.read_csv('customers.csv')

st.set_page_config(layout="wide")

cmp_p, vlncat_p, vlnnum_p, pairplot_p = sidebar()

row1 = st.columns(2)
row2 = st.columns(2)

grid = [col.container(border=False) for col in row1 + row2]


with grid[0]:

  fig = plot_bar(df)
  st.metric(label="Customers", value=df.shape[0])
  st.pyplot(fig)


with grid[1]:

  campain = choose_overall(cmp_p)
  fig = px.sunburst(df, path=[campain, 'Complain', 'Marital', 'Education',])
  st.plotly_chart(fig)

with grid[2]:

  cat = vlncat_p
  num = vlnnum_p
  campain = choose_overall(cmp_p)
  val_cat = ('Not Accepted','Accepted')
  fig =plot_violin(df,campain,cat,val_cat)
  st.plotly_chart(fig)

with grid[3]:

  if not pairplot_p:
    pairplot_p = ['Income','Recency','MntWines']
    
  fig = sns.pairplot(df[pairplot_p+[campain]], hue=campain)  
  
#  for ax in fig.axes.flatten():
#    ax.set_xscale('log')
#    ax.set_yscale('log')

  st.pyplot(fig)


st.header("Data Descriptions")
            
# Data descriptions as a dictionary
data_descriptions = {
  "Attribute": [
      "Complain", "Education", "Marital", "Kidhome", 
      "Teenhome", "Income", "Mnt", "Recency", 
      "NumWebVisitsMonth", "NumWebPurchases"
  ],
  "Description": [
      "Indicates if the customer has complained in the last 2 years.",
      "The customer's level of education.",
      "The customer's marital status.",
      "Number of small children in the customer's household.",
      "Number of teenagers in the customer's household.",
      "The customer's yearly household income.",
      "Amount spent on a specific product in the last 2 years.",
      "Number of days since the last purchase.",
      "Number of visits to the company's website in the last month.",
      "Number of purchases made through the company's website."
  ]
}

# Create DataFrame
df_descriptions = pd.DataFrame(data_descriptions)
# Display DataFrame as a table
st.table(df_descriptions)


  