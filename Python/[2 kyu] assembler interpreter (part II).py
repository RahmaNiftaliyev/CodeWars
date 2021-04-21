# see https://www.codewars.com/kata/58e61f3d8ff24f774400002c/train/python

from TestFunction import Test

cmp_output = {}
memory = {}
output = ''
code = ''
functions = {}

def execute_command(command):
  global cmp_output, memory, output, code
  cmd = command.strip().split(" ")[0]
  print(command, memory, output)
  if cmd == 'mov':
    tmp_command = command.strip()[3:].strip()
    x, y = tmp_command.split(",")[0].strip(), tmp_command.split(",")[1].strip()
    if not y.isalpha():
      if y.isdigit():
        memory[x] = int(y)
      else:
        memory[x] = float(y)
    else:
      if y in memory:
        memory[x] = memory[y]
    return
  elif cmd == 'cmp':
    tmp_command = command.strip()[3:].strip()
    x, y = tmp_command.split(",")[0].strip(), tmp_command.split(",")[1].strip()
    val_x, val_y = None, None
    if not x.isalpha():
      if x.isdigit():
        val_x = int(x)
      else:
        val_x = float(x)
    else:
      if x in memory:
        val_x = memory[x]
    if not y.isalpha():
      if y.isdigit():
        val_y = int(y)
      else:
        val_y = float(y)
    else:
      if y in memory:
        val_y = memory[y]
    cmp_output = {'x': val_x, 'y': val_y}
    return
  elif cmd == 'msg':
    tmp_command = str(command.strip()[3:].strip())
    i = 0
    while i < len(tmp_command):
      if tmp_command[i] == "'" and i+1 != len(tmp_command):
        j = i + 1
        while tmp_command[j] != "'":
          j += 1
        output += tmp_command[i+1:j]
        i = j + 1
      elif tmp_command[i].isalpha():
        if tmp_command[i] in memory:
          output += str(memory[tmp_command[i]])
        i += 1
      else:
        i += 1
    return 
  elif cmd == 'inc':
    if command.strip().split(" ")[-1] in memory:
      memory[command.strip().split(" ")[-1]] += 1
    return
  elif cmd == 'dec':
    if command.strip().split(" ")[-1] in memory:
      memory[command.strip().split(" ")[-1]] -= 1
    return
  elif cmd == 'add' or cmd == 'sub' or cmd == 'mul' or cmd == 'div':
    tmp_command = command.strip()[3:].strip()
    x, y = tmp_command.split(",")[0].strip(), tmp_command.split(",")[1].strip()
    if not y.isalpha():
      if y.isdigit():
        val = int(y)
      else:
        val = float(y)
    else:
      if y in memory:
        val = memory[y]
    if x in memory:
      if cmd == 'add':
        memory[x] += val
      elif cmd == 'sub':
        memory[x] -= val
      elif cmd == 'mul':
        memory[x] *= val
        memory[x] = int(memory[x])
      elif cmd == 'div':
        if val != 0 and val != 0.0:
          memory[x] /= val
          memory[x] = int(memory[x])
    return
  elif cmd == 'jne':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] != cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'je':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] == cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'jge':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] >= cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'jg':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] > cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'jle':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] <= cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'jl':
    function_name = command.strip()[3:].strip()
    if cmp_output['x'] < cmp_output['y']:
      call_function(function_name)
    return
  elif cmd == 'jmp':
    function_name = command.strip()[3:].strip()
    call_function(function_name)
    return
  elif cmd == 'call':
    function_name = command.strip()[4:].strip()
    call_function(function_name)
    return
  elif cmd == 'ret':
    return
  elif cmd == 'end':
    return output
  else:
    return
  
def call_function(function_name):
  global cmp_output, memory, output, code
  i = 0
  while i < len(code.splitlines()):
    if function_name in code.splitlines()[i] and code.splitlines()[i].split()[0] not in ['call', 'jl', 'jle', 'jmp', 'jne', 'je', 'jge', 'jg']:
      while code.splitlines()[i+1][:4] == "    ":
        if code.splitlines()[i+1].strip() == 'ret':
          i = len(code.splitlines())
          functions[function_name] = True
          break
        ret, command = remove_comments(code.splitlines()[i+1])
        if ret:
          execute_command(command)
        i += 1
        if i + 1 >= len(code.splitlines()):
          break
    i += 1
  return
  
def remove_comments(command):
  if ';' in command:
    command = command[:command.find(';')]
  if command == "":
    return False, command
  return True, command

def assembler_interpreter(program, recur=None):
  global cmp_output, memory, output, code
  if not recur:
    code = (program + '.')[:-1]
  pointer = 0
  program = program.splitlines()
  while pointer < len(program):
    ret, program[pointer] = remove_comments(program[pointer])
    if not ret:
      pointer += 1
      continue
    cmd = program[pointer].strip().split(" ")
    command = cmd[0]
    execute_command(program[pointer])
    if command == 'end':
      for func in functions:
        if not functions[func]:
          return -1
      return output
    elif command == 'ret':
      return
    pointer += 1
  return -1


test = Test(None)

""" ============================================================== """

# program = '''
# ; My first program
# mov  a, 5
# inc  a
# cmp   a, 1
# add   a, 2
# sub a, 2
# mul a,  5
# div  a, 8
# msg  '(5+1)/2 = ', a    ; output message
# end
# '''

# test.assert_equals(assembler_interpreter(program), '(5+1)/2 = 3')

""" ============================================================== """

# program = '''
# ; My first program
# mov  a, 5
# inc  a
# call function
# msg  '(5+1)/2 = ', a    ; output message
# end

# function:
#     div  a, 2
#     ret
# '''

# test.assert_equals(assembler_interpreter(program), '(5+1)/2 = 3')

""" ============================================================== """

# program_factorial = '''
# mov   a, 5
# mov   b, a
# mov   c, a
# call  proc_fact
# call  print
# end

# proc_fact:
#     dec   b
#     mul   c, b
#     cmp   b, 1
#     jne   proc_fact
#     ret

# print:
#     msg   a, '! = ', c ; output text
#     ret
# '''

# test.assert_equals(assembler_interpreter(program_factorial), '5! = 120')

""" ============================================================== """

# program_mod = '''
# mov   a, 11           ; value1
# mov   b, 3            ; value2
# call  mod_func
# msg   'mod(', a, ', ', b, ') = ', d        ; output
# end

# ; Mod function
# mod_func:
#     mov   c, a        ; temp1
#     div   c, b
#     mul   c, b
#     mov   d, a        ; temp2
#     sub   d, c
#     ret
# '''

# test.assert_equals(assembler_interpreter(program_mod), 'mod(11, 3) = 2')

""" =============================================================== """

# program_fibonacci = '''
# mov   a, 8            ; value
# mov   b, 0            ; next
# mov   c, 0            ; counter
# mov   d, 0            ; first
# mov   e, 1            ; second
# call  proc_fib
# call  print
# end

# proc_fib:
#     cmp   c, 2
#     jl    func_0
#     mov   b, d
#     add   b, e
#     mov   d, e
#     mov   e, b
#     inc   c
#     cmp   c, a
#     jle   proc_fib
#     ret

# func_0:
#     mov   b, c
#     inc   c
#     jmp   proc_fib

# print:
#     msg   'Term ', a, ' of Fibonacci series is: ', b        ; output text
#     ret
# '''

# test.assert_equals(assembler_interpreter(program_fibonacci), 'Term 8 of Fibonacci series is: 21')

""" ============================================================== """

# program_gcd = '''
# mov   a, 81         ; value1
# mov   b, 153        ; value2
# call  init
# call  proc_gcd
# call  print
# end

# proc_gcd:
#     cmp   c, d
#     jne   loop
#     ret

# loop:
#     cmp   c, d
#     jg    a_bigger
#     jmp   b_bigger

# a_bigger:
#     sub   c, d
#     jmp   proc_gcd

# b_bigger:
#     sub   d, c
#     jmp   proc_gcd

# init:
#     cmp   a, 0
#     jl    a_abs
#     cmp   b, 0
#     jl    b_abs
#     mov   c, a            ; temp1
#     mov   d, b            ; temp2
#     ret

# a_abs:
#     mul   a, -1
#     jmp   init

# b_abs:
#     mul   b, -1
#     jmp   init

# print:
#     msg   'gcd(', a, ', ', b, ') = ', c
#     ret
# '''

# test.assert_equals(assembler_interpreter(program_gcd), 'gcd(81, 153) = 9')

""" ============================================================== """

program_fail = '''
call  func1
call  print
end

func1:
    call  func2
    ret

func2:
    ret

print:
    msg 'This program should return -1'
'''

test.assert_equals(assembler_interpreter(program_fail), -1)

""" ============================================================== """
