def run_program(program):
  ram = []
  for i in range(16):
    ram.append(0)

  # Registers
  registers = []
  for i in range(16):
    registers.append(0)

  # Program counter
  pc = 0

  #accumulator
  accumulator = 0

  # Program loop
  while pc < len(program):
    instruction = program[pc].split()
    opcode = instruction[0]

    try:
      if opcode == "loadToRam":
        address = int(instruction[1])
        value = int(instruction[2])
        ram[address] = value

      elif opcode == "loadToReg":
        address = int(instruction[1])
        value = int(instruction[2])
        registers[address] = value

      elif opcode == "load_RAM_to_register":
        address = int(instruction[1])
        register = int(instruction[2])
        registers[register] = ram[address]

      elif opcode == "add":
        register1 = int(instruction[1])
        register2 = int(instruction[2])
        accumulator = registers[register1] + registers[register2]

      elif opcode == "sub":
        register1 = int(instruction[1])
        register2 = int(instruction[2])
        accumulator = registers[register1] - registers[register2]

      elif opcode == "store_to_RAM":
        address = int(instruction[1])
        register = int(instruction[2])
        ram[address] = registers[register]

      elif opcode == "jump_if_0":
        address = int(instruction[1])
        if accumulator == 0:
          pc = address
          continue  # Skip incrementing pc

      elif opcode == "jump_if_not_0":
        address = int(instruction[1])
        if accumulator != 0:
          pc = address
          continue  # Skip incrementing pc

      elif opcode == "jump":
        address = int(instruction[1])
        pc = address
        continue  # Skip incrementing pc

      elif opcode == "output":
        address = int(instruction[1])
        print(f"Output: {ram[address]}")

      elif opcode == "StoreAccumator":
        register = int(instruction[1])
        registers[register] = accumulator

      # Increment program counter
      pc += 1
    except Exception as e:
      exit(f"Error: {e} on line {pc}: \n {program[pc]}")
