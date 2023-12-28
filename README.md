# Algorithm for resolving propositional logic

This repository contains the source code, input, and output for the propositional logic resolving algorithm. Given a knowledge base **(KB)** and an $\alpha$ sentence, they are represented by propositional logic and normalized to the standard form CNF. Determine "**KB** entails $\alpha$" (**KB** $\vDash \alpha$) by resolving.

**Description of input and output data**

- **Input data**: **KB** and $\alpha$ in CNF standard format are saved in the file **input.txt**. The file has the following conventional format:
     - The first line contains the sentence $\alpha$
     - The second line contains the integer N - the number of clauses in the KB
     - The next N lines represent clauses in the KB, one clause per line

Positive literals are represented by single capital letters (A-Z). Negative literals are positive literals with a minus sign (‘-‘) right before the character

The OR keyword joins literals together. There can be one or more spaces between literals and the OR keyword

- **Output data**: The set of propositions generated during the solution process and the conclusion are saved in the file **output.txt**. The file has the following conventional format:
     - The first line contains the integer $M_1$ - the number of clauses generated in the first loop. The next $M_1$ lines represent the clauses generated in the first loop (including the empty clause), one clause per line. Empty clauses are represented by the string “{}”
     - The next loops (with $M_2$, $M_3$,..., $M_n$ clauses respectively) are performed similarly as above
     - The last line presents the conclusion, that is, answers the question “**KB** entails $\alpha$?”. Print YES if **KB** entails $\alpha$. On the contrary, print NO.
     - Ignore duplicate clauses (appearing in the same loop, original KB, or previous loops).


- Literals in the same clause (for both input and output data) are arranged in alphabetical order
- Propositions of the form $A \vee B \vee -B$ have truth value $True$ because they are equivalent to $A \vee True$. Such clauses are useless for inference and can therefore be omitted

Instructions for running source code:
- Place the input data as described in the `input` folder
- Run the `pl_resolution.py` file
- Receive output data in the `output` folder
- Make sure that the `input`, `output` folders, and `pl_resolution` files are always in the same directory
