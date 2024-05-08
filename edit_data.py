import pandas as pd

def delete_columns(df):
    # Delete specified columns
    columns_to_drop = ['FEN', 'output', 'FEN + Next move', 'NL Format of FEN + Next move', 'Output for NLP']
    df.drop(columns=columns_to_drop, inplace=True)
    print("Columns deleted successfully.")

def update_instruction_column(df):
    # Update existing 'instruction' column with new content
    #df['Instruction'] = ("You are a chess grandmaster. You understand and can locate chess pieces given the current state of the chess board in Forsyth Edwards Notation (FEN). Given a board's state in FEN, your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to describe what next move would result in the best centipawn improvement for the active player. You will describe the move by giving a piece starting and ending coordinates (e.g., d4e5). Take extra care to only respond with a valid, legal move. ")
    #print("Column 'instruction' updated  successfully.")
    print(df['FEN_input'].iloc[0])
def edit_fen_input_column(df):
    #df.drop(columns=['FEN_input'], inplace=True)
    df['FEN_input'] = "The board is in the following position: " + '"' + df['FEN'] + '". ' + "What next move would produce the best centipawn improvement for the active player?"
    #df.insert(1, 'FEN_input', FEN_input)
    df['FEN_and_Languages_ver'] = "Here is the FEN state: "  + '"' + df['FEN'] + '". ' + "And here is the language version of the corresponding FEN state: " + df['NL Format of FEN']
def edit_fen_output(df):
    df['FEN_output'] = df['FEN_output'].str.split('The best move of this fen state is:').str.join('The next move which would produce the best centipawn improvement for the active player of this fen state is:')
    print("Column 'FEN_input' updated successfully.")

def modify_NL_format(df):
    # Modify the NL format
    #df['NL Format of FEN'] = df['NL Format of FEN'] + " What next move would produce the best centipawn improvement for the active player?"
    df['Output for NLP'] = df['Output for NLP'].str.replace("the output is", "The next move which would produce the best centipawn improvement for the active player of this board state is", regex=False)
    print("Columns updated successfully.")
    
def edit_fen_language_ver(df):
    #df['FEN_and_Languages_ver'] = df['FEN_and_Languages_ver'] + " What next move would produce the best centipawn improvement for the active player?"
    df = df.rename(columns={'Instruction': 'Instruction_fen'})

def add_instruction_nl_column(df):
    # Create new column 'instruction_nl' with the specified content
    instruction_nl = ("You are a chess grandmaster. Given a spoken-language description of a board's state, your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to describe what next move would result in the best centipawn improvement for the active player. You will describe the move by giving a piece starting and ending coordinates (e.g., d4e5). Take extra care to only respond with a valid, legal move.")
    #adjust the position of column as desired
    df.insert(7, 'instruction_nl', instruction_nl)
    print("Column 'instruction_nl' added successfully at the 7th position.")

def add_instruction_fen_nl_column(df):
    # Create new column 'instruction_fen_nl' with the specified content
    instruction_fen_nl = ("You are a chess grandmaster. You understand and can locate chess pieces given the FEN state and the description of current state of the chess board. Your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to find the next move that produce the best centipawn improvement for the active player. You will describe the move by giving a starting square of piece and ending square as coordinates of board . Take extra care to only use legal and valid move.")
    #adjust the position of column as desired
    df.insert(3, 'instruction_fen_nl', instruction_fen_nl)
    print("Column 'instruction_fen_nl' added successfully at the 3rd position.")

def main():
    file_path = "FEN_DATABASE_train_30k.csv"

    # Read the CSV file
    with open(file_path, 'r') as file:
        df = pd.read_csv(file)

    # Perform data modifications
    #edit_fen_input_column(df)
    update_instruction_column(df)
    #edit_fen_output(df)
    #modify_NL_format(df)
    #add_instruction_nl_column(df)
    #add_instruction_fen_nl_column(df)
    #edit_fen_language_ver(df)
    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)



if __name__ == "__main__":
    main()
