from os import listdir

def read_input(file_name, kb_a):
    """Read file data and store it in the designed data structure"""
    with open(file_name, 'r') as f:
        read_data = f.readlines()  # Read all data into a list
        for i in range(len(read_data)):
            read_data[i] = read_data[i].strip()  # Remove '\n' at the end of each line
            read_data[i] = read_data[i].replace(" OR", "")  # Remove OR operations
        kb_a["number_of_clause"] = int(read_data[1])  # Save the number of clauses in KB
        read_data.pop(1)  # Remove the line containing the number of clauses in KB
        for line in read_data:
            clause = []
            line_splitted = line.split()  # Split strings containing literals in the clause
            # Save literals in the clause
            for literal in line_splitted:
                if len(literal) == 1:
                    clause.append([literal, 1])  # Save positive literal in the clause
                else:
                    clause.append([literal[1], 0])  # Save negative literal in the clause
            kb_a["KB"].append(clause)  # Add the clause to KB

        kb_a["alpha"] = kb_a["KB"][0]  # Save the alpha clause
        kb_a["KB"].pop(0)  # Remove the alpha clause from KB


def sort_literal(e):
    """Function for sorting literals in the clause in alphabetical order"""
    return e[0]  # Return the alphabetical order of the literal


def negate_literal(literal):
    """Function to negate a literal"""
    return [literal[0], (literal[1] + 1) % 2]  # Change 0 to 1 and 1 to 0 to negate


def transform_literal(literal):
    """Function to transform the data structure storing the literal into a string containing the literal"""
    result = ""
    if literal[1] == 0:
        result += "-"  # Add - sign if it is a negative literal
    result += literal[0]
    return result


def transform_clause(clause):
    """Function to transform the data structure storing the clause into a string containing the CNF form of the clause"""
    sentence = ""
    for literal in clause:
        sentence = sentence + transform_literal(literal) + " OR "
    sentence = sentence[:-4] + '\n'  # Remove the extra OR and add a newline character
    return sentence


def pl_resolve(ci, cj):
    """Function to resolve 2 clauses and return the resulting clause if the conditions are satisfied"""
    resolvents = None
    negated_literal = []
    ci_copy = ci.copy()  # Create a copy of the two clauses to avoid modifying the original clauses
    cj_copy = cj.copy()
    # Negate literals in clause ci and check if there exist negated literals in clause cj, if yes, resolve
    for literal in ci:
        negated_literal = negate_literal(literal)
        if negated_literal in cj:
            resolvents = []
            # Remove the two resolved literals
            ci_copy.remove(literal)
            cj_copy.remove(negated_literal)
            # Save the remaining literals in the resulting resolved clause
            resolvents.extend(ci_copy)
            resolvents.extend(cj_copy)
            break
    # If the result is an empty clause
    if resolvents == []:
        return [["{}", 1]]
    # If no resolution is possible
    if resolvents is None:
        return None
    # Filter out duplicate literals in the resolved clause, keep only one of each type
    result = []
    for literal in resolvents:
        if literal not in result:
            result.append(literal)
    resolvents = result
    # Sort literals in alphabetical order
    resolvents.sort(key=sort_literal)
    # If the result is a clause of the form A OR B OR -B, remove it as it is redundant
    for literal in resolvents:
        negated_literal = negate_literal(literal)
        if negated_literal in resolvents:
            return None
    # Return the result
    return resolvents


def pl_resolution(kb_a):
    """Resolution algorithm, return a list containing data to be written to the result file"""
    clauses = kb_a["KB"]  # Get the list of clauses in KB
    alpha = kb_a["alpha"]  # Get the alpha clause
    result = ""  # Variable to store the conclusion
    written_data = []  # List containing data to be written to the result file
    # Negate literals in the alpha clause and add to KB
    for literal in alpha:
        clauses.append([negate_literal(literal)])
    # Iterate until an empty clause is resolved or no more new clauses can be generated from the current KB
    while True:
        new = []  # List to store clauses generated in each iteration
        clause_generated = []  # List of new clauses that can be added to KB
        # Iterate through each pair of clauses in KB
        for i in range(len(clauses) - 1):
            for j in range(i + 1, len(clauses)):
                resolvents = pl_resolve(clauses[i], clauses[j])  # Resolve the two clauses being iterated
                # If the new clause is not already in new, add it to new
                if resolvents is not None and resolvents not in new:
                    new.append(resolvents)
        # Filter out clauses generated in this iteration that are not already in the current KB
        m = 0
        for new_clause in new:
            if new_clause not in clauses:
                m += 1
                clauses.append(new_clause)
                clause_generated.append(transform_clause(new_clause))
        # Add data to the list containing data to be written to the result file
        written_data.append(str(m) + '\n')
        written_data.extend(clause_generated)
        # If no more new clauses can be generated from the current KB, conclude with "NO"
        if m == 0:
            result = "NO"
            break
        # If an empty clause is resolved, conclude with "YES"
        if [["{}", 1]] in new:
            result = "YES"
            break
    # Add the conclusion sentence
    written_data.append(result)
    return written_data


def write_output(file_name, written_data):
    """Function to write data from the list to a file, each element in the list is a line in the file"""
    with open(file_name, 'w') as f:
        for line in written_data:
            f.write(line)


if __name__ == "__main__":
    """Main function to read data from input files in the directory, execute the resolution algorithm,
    and write output data to files in another directory"""
    input_path = "input/"
    output_path = "output/"
    input_files = [f for f in listdir(input_path)]  # List input files
    # Perform resolution for each KB and alpha from the input files
    for input_file in input_files:
        kb_a = {
            "alpha": [],
            "number_of_clause": 0,
            "KB": []
        }
        read_input(input_path + input_file, kb_a)
        written_data = pl_resolution(kb_a)
        write_output(output_path + input_file.replace("in", "out"), written_data)