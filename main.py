import emulator
UsedAddresses = []
Variables = {}
Subroutines = {}


def FileToList(path):
  with open(path, 'r') as file:
    lines = [
        line.strip() for line in file if not line.strip().startswith('//')
    ]
  return lines


def Find_Next_Address():
  global UsedAddresses
  length = len(UsedAddresses)
  if length == 0:
    UsedAddresses.append(0)
    return 0
  for i in range(length):
    if i not in UsedAddresses:
      UsedAddresses.append(i)
      return i
  UsedAddresses.append(length)
  return length


def ProsessLine(line):
  global Variables
  global UsedAddresses

  assembly_instructions = []
  
  # Check if the line is a variable declaration
  if line.startswith("var"):
    parts = line.split()
    if len(parts) >= 5 and parts[3] == "=":
      var_type = parts[1]
      var_name = parts[2]
      var_value = parts[4]

      #make sure language supports type
      if var_type not in ["int", "bool"]:
        exit(f"Error: Unsupported type '{var_type}' for variable '{var_name}'")

      # Assign a RAM address (simple increment for this example)
      if var_name not in Variables:
        Variables[var_name] = {
            'type': var_type,
            'address': Find_Next_Address()
        }
        print(
            f"Variable {var_name} of type {var_type} assigned RAM address {Variables[var_name]['address']}"
        )
        # Generate assembly instruction to load value into memory
        if var_type == "int":
          assembly_instructions.append(
              f"loadToRam {Variables[var_name]['address']} {var_value}")
        elif var_type == "bool":
          if var_value == "true":
            assembly_instructions.append(
                f"loadToRam {Variables[var_name]['address']} 0")
          elif var_value == "false":
            assembly_instructions.append(
                f"loadToRam {Variables[var_name]['address']} 1")
      else:
        exit(f"Error: Variable {var_name} already declared")
  # Check if the line is a variable assignment with arithmetic operations
  elif "=" in line:
    parts = line.split("=")
    if len(parts) == 2:
      var_name = parts[0].strip()
      if var_name in Variables:
        # Check for arithmetic operations
        if "+" in parts[1] or "-" in parts[1]:
          # Split the expression to get operands
          operands = line.split("=")[1].split("=")[0].split(
              "+") if "+" in line else line.split("=")[1].split("=")[0].split(
                  "-")
          if len(operands) == 2:
            operand1 = operands[0].strip()
            operand2 = operands[1].strip()
            result_var = parts[0].strip()  # The variable to store the result

            if Variables[result_var]["type"] == "int" and Variables[operand1][
                "type"] == "int" and Variables[operand2]["type"] == "int":

              # Load operands into registers
              if operand1 in Variables:
                assembly_instructions.append(
                    f"load_RAM_to_register {Variables[operand1]['address']} 1"
                )
              if operand2 in Variables:
                assembly_instructions.append(
                    f"load_RAM_to_register {Variables[operand2]['address']} 2"
                )

              # Perform the operation
              if "+" in line:
                assembly_instructions.append("add 0 1")
              elif "-" in line:
                assembly_instructions.append("sub 0 1")

              assembly_instructions.append("StoreAccumator 3")

              # Store the result back to memory
              if result_var in Variables:
                assembly_instructions.append(
                    f"store_to_RAM {Variables[result_var]['address']} 3")
              else:
                exit(f"Error: Variable {result_var} not declared")
            else:
              exit(
                  "Error: Only integer variables can be used for arithmetic operations"
              )
      else:
        exit(f"Error: Variable {var_name} not declared")

  elif line.startswith("delete"):
    parts = line.split()
    if parts[1] in Variables:
      UsedAddresses.remove(Variables[parts[1]]['address'])
      del Variables[parts[1]]
  elif line.startswith("out("):
    # Extract the variable name
    var_name = line[4:-1]
    if var_name in Variables:
        # Generate assembly instruction to output the value of the variable
        assembly_instructions.append(f"output {Variables[var_name]['address']}")
    else:
        print(f"Error: Variable {var_name} not declared")

  return assembly_instructions


def SetALUoutputToBool(condition, assembly_instructions):
  trueAddress = -1
  blankAddress = -1
  if condition == "true":
    trueAddress = Find_Next_Address()
    blankAddress = Find_Next_Address()
    assembly_instructions.append(f"loadToRam {trueAddress} 0")
    assembly_instructions.append(f"add {trueAddress} {blankAddress}")
  elif condition == "false":
    trueAddress = Find_Next_Address()
    blankAddress = Find_Next_Address()
    assembly_instructions.append(f"loadToRam {trueAddress} 1")
    assembly_instructions.append(f"add {trueAddress} {blankAddress}")
  elif condition in Variables:
    if Variables[condition]["type"] == "bool":
      blankAddress = Find_Next_Address()
      assembly_instructions.append(
          f"add {blankAddress} {Variables[condition]['address']}")
    else:
      exit("Cannot use while loop with non-boolean condition")
  if blankAddress != -1:
    UsedAddresses.remove(blankAddress)
  if trueAddress != -1:
    UsedAddresses.remove(trueAddress)


def CompileFile(path):
  global UsedAddresses
  global Variables
  assembly_instructions = []
  temp = [[], [], [], [], [], []]
  nesting_val = 0

  inWhileLoop = False
  inIfStatement = False
  condition = None
  startLoop =  [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]

  fileList = FileToList(path)
  for line in fileList:
      parts = line.split()
      if len(parts) >=  1:
          # Handling while loops
          if parts[0] == "while" and not inWhileLoop:
              cparts = line.split('(')
              if len(cparts) >  1:
                  condition = cparts[1].split(')')[0].strip()
              inWhileLoop = True
              startLoop[nesting_val] = len(assembly_instructions)
              nesting_val += 1

          elif inWhileLoop:
              if parts[0] == "}":
                  SetALUoutputToBool(condition, assembly_instructions)
                  assembly_instructions.append(f"jump_if_0 {len(assembly_instructions) +  1}")
                  assembly_instructions.extend(temp[nesting_val])
                  assembly_instructions.append(f"jump {startLoop[nesting_val]}")
                  inWhileLoop = False
                  nesting_val -= 1
              elif parts[0] != "}" or parts[0] != "{":
                temp[nesting_val].extend(ProsessLine(line))

          # Handling if statements
          if parts[0] == "if" and not inIfStatement:
              cparts = line.split('(')
              if len(cparts) >  1:
                  condition = cparts[1].split(')')[0].strip()
              inIfStatement = True

          elif inIfStatement:
              if parts[0] == "}":
                  SetALUoutputToBool(condition, assembly_instructions)
                  assembly_instructions.append(f"jump_not_0 {(len(assembly_instructions) - 1) + len(temp[nesting_val])}")
                  assembly_instructions.extend(temp[nesting_val])
                  inIfStatement = False
              elif parts[0] != "}" or parts[0] != "{":
                temp[nesting_val].extend(ProsessLine(line))

          else:
            assembly_instructions.extend(ProsessLine(line))

  with open("assembly_output.asmbl", 'w') as file:
      for instruction in assembly_instructions:
          file.write(instruction + '\n')


#compiler main
file_path = str(input("Enter the path to the file you wish to compile: \n"))
CompileFile(file_path)

# Run the compiled program
program = FileToList("assembly_output.asmbl")
emulator.run_program(program)