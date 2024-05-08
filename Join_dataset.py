import pandas as pd

# # file_path = "FEN_STATE_DATABASE_v2.csv"
# # df = pd.read_csv(file_path)


# # df.insert(0, 'instruction', "You are a chess grandmaster. you understand and are able to locate chess pieces on the board given its FEN state. Your task is to find the best next move in the chess game given the FEN state. You will describe the best next move by giving a piece’s starting square and ending square using algebraic notation describing both coordinates. Take extra care to only use legal and valid move. ")
# # df.to_csv(file_path, index=False)

# # print("New column 'instruction' added successfully at the beginning.")

# #Read the two tables from files
# # table1 = pd.read_csv('FEN DATABASE.csv')
# # table2 = pd.read_csv('FEN_DATABASE_v2.csv')

# # # Concatenate the rows of both tables
# # merged_table = pd.concat([table1, table2])

# # # Save the merged table to a new file
# # merged_table.to_csv('FEN_STATE_DATABASE_v2.csv', index=False)

# # print("Merged table saved to 'merged_FEN_DATABASE.csv'")


# import pandas as pd

# # Load your csv file
# df = pd.read_csv('FEN_STATE_DATABASE_v2.csv')

# # Define a function to create the desired string
# def create_input_string(fen):
#     return f'The board is in the following position: {fen}. What is the best next move?'

# def create_output_string(output):
#     return f'The best move of this fen state is: {output}'

# def create_FEN_NLP_string(row):
#     return f'Here is the FEN state: {row["FEN"]}. And here is the language version of its: {row["NL Format of FEN"]}.'

# # Apply the function to the 'FEN' column and create a new column 'FEN_input'
# df.insert(1, 'FEN_input', df['FEN'].apply(create_input_string))

# # Apply the function to the 'output' column and create a new column 'FEN_output'
# df.insert(2, 'FEN_output', df['output'].apply(create_output_string))

# # Apply the function to the DataFrame and create a new column 'FEN_and_Languages_ver'
# df.insert(3, 'FEN_and_Languages_ver', df.apply(create_FEN_NLP_string, axis=1))

# # Save the dataframe back to csv with a new name
# df.to_csv('FEN_STATE_DATABASE_v2_with_input.csv', index=False)

df = pd.read_csv('FEN_STATE_DATASET_v3.csv')
# Extract the first 10 rows
df_first_10 = df.head(10)

# Save the dataframe with only the first 10 rows to csv with a new name
df_first_10.to_csv('FEN_STATE_DATABASE_v2_first_10.csv', index=False)