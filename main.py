import streamlit as st
from cjkradlib import RadicalFinder
from functools import lru_cache
from helper import *

EXCLUSION = (
        set('⿰⿱⿸⿺⿳⿻⿵⿲⿹⿴⿷⿶？')
        # | set(chr(i) for i in range(ord('①'), ord('⑳') + 1))
)

finder = RadicalFinder(lang='zh')  # default is 'zh'

dfDictData=pd.read_pickle('04dfRadicalZFL.pkl')
dfDictData=dfDictData[['character','one','radical']]
dfbothu=pd.read_pickle('05bothu.pkl')

def main():
    st.title("Chinese Character Radicals Finder")

    paragraph = st.text_area("Enter a paragraph in Chinese:", height=200)
    paragraph=extract_chinese_characters(paragraph)
    dfDecomposition=filter_dataframe_by_character(df=dfDictData,character_tuple=paragraph,column_name='character')
    listDecomposition=dfDecomposition['radical'].str.cat()
    listDecomposition=extract_chinese_characters(listDecomposition)
    listDecomposition= list(dict.fromkeys(listDecomposition))
    
    temp_df = pd.DataFrame({'radical': listDecomposition})
    temp_df['temp_index'] = range(len(temp_df))
    dfRadical=lookup_and_copy_values(dfMain=temp_df,dfMainColumn='radical',dfSub=dfbothu,dfSubColumn='radical')
    
    # st.write(*listDecomposition)
    if len(dfRadical)>0:
        st.success(f"Radical to learn: {len(dfRadical)}")
        with st.expander("Start to learn"):
            dfRadical=dfRadical[['radical_y','name','pinyin','meaning','stroke']]
            dfRadical=dfRadical.dropna()
            dfRadical=dfRadical.reset_index()
            dfRadical=dfRadical[['radical_y','name','pinyin','meaning','stroke']]
            st.dataframe(dfRadical)
    if len(dfDecomposition)>0:  
        with st.expander("See full database"):
            dfDecomposition

if __name__ == "__main__":
    main()
