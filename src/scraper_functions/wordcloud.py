import pandas as pd
import os
from collections import Counter
import re

def analyze_text(excel_path: str, 
                target_column: str, 
                filter_column: str = None, 
                filter_value: str = None,
                output_folder: str = None):
    """
    Extract text from Excel, filter, remove stopwords, and output ranked word count.
    
    Usage from terminal:
    python word_analysis.py
    """
    
    # Set output folder
    if output_folder is None:
        output_folder = os.path.dirname(excel_path)
    os.makedirs(output_folder, exist_ok=True)
    
    # Read Excel
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        print(f"Loaded {len(df)} rows")
    except Exception as e:
        print(f"ERROR: {e}")
        return None
    
    # Check columns
    if target_column not in df.columns:
        print(f"Column '{target_column}' not found")
        print(f"Available: {df.columns.tolist()}")
        return None
    
    # Apply filter
    if filter_column and filter_value:
        if filter_column not in df.columns:
            print(f"Filter column '{filter_column}' not found")
            return None
        df = df[df[filter_column] == filter_value]
        print(f"Filtered to {len(df)} rows where {filter_column} = '{filter_value}'")
    
    # Get text
    text_data = df[target_column].dropna().astype(str)
    if len(text_data) == 0:
        print(" No data to analyze")
        return None
    
    # Clean and split
    all_text = ' '.join(text_data.values)
    cleaned_text = re.sub(r'[^\w\s]', ' ', all_text.lower())
    words = cleaned_text.split()
    
    # Remove stopwords
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'their', 'them', 'what', 'which', 'who', 'when', 'where', 'why', 'how',
        'its', 'our', 'your', 'all', 'each', 'some', 'more', 'most', 'other'
    }
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count and rank
    word_freq = Counter(filtered_words)
    word_count_df = pd.DataFrame(word_freq.most_common(), columns=['Word', 'Count'])
    word_count_df['Rank'] = range(1, len(word_count_df) + 1)
    word_count_df = word_count_df[['Rank', 'Word', 'Count']]
    
    # Save
    filter_suffix = f"_{filter_value.replace(' ', '_')}" if filter_value else ""
    output_filename = f"{target_column.replace(' ', '_')}_wordcount{filter_suffix}.xlsx"
    output_path = os.path.join(output_folder, output_filename)
    
    word_count_df.to_excel(output_path, index=False, sheet_name='Word Count')
    print(f"\nSaved to: {output_path}")
    print(f"Found {len(word_count_df)} unique words\n")
    print(word_count_df.head(10).to_string(index=False))
    
    return word_count_df


if __name__ == "__main__":
    # Run your analysis here
    analyze_text(
        excel_path=r"C:\wordcloud\Operational Plan Tracker.xlsx",
        target_column="Value to Client",
        filter_column="Accountable Manager",
        filter_value="Reese Baguio",
        output_folder=r"C:\wordcloud"
    )