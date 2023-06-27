import sys
from subprocess import run, STDOUT, PIPE

SEP = ' => '

def getAllFiles():
    command = run(f'ls'.split(), stdout=PIPE, stderr=STDOUT, text=True)
    files = []
    for file in command.stdout.split('\n'):
        if file.split('.')[:-2:-1][0] == 'c':
            files.append('.'.join(file.split('.')[:-1]))
    return files

def parseArgv(argv):
    flags = {
        'compile': False,
        'format': False,
        'test': False,
        'verterTest': False,
        'styleTest': False,
        'compileTest': False,
        'leaksTest': False,
        'runtimeTest': False,
        'all': False
    }
    files = []
    for arg in argv:
        if len(arg) > 1 and arg[0] == '-' and arg[1] != '-':
            if 'c' in arg:
                flags['compile'] = True
            if 'f' in arg:
                flags['format'] = True
            if 't' in arg:
                flags['test'] = True
                flags['verterTest'] = True
                flags['styleTest'] = True
                flags['compileTest'] = True
                flags['leaksTest'] = True
                flags['runtimeTest'] = True
            if 'a' in arg:
                flags['all'] = True
            if 'V' in arg:
                flags['verterTest'] = True
            if 'S' in arg:
                flags['styleTest'] = True
            if 'C' in arg:
                flags['compileTest'] = True
            if 'L' in arg:
                flags['leaksTest'] = True
            if 'R' in arg:
                flags['runtimeTest'] = True
        elif len(arg) > 2 and arg[0:2] == '--' and arg[2] != '-':
            if arg == '--compile':
                flags['coompile'] = True
            if arg == '--format':
                flags['format'] = True
            if arg == '--test':
                flags['test'] = True
                flags['verterTest'] = True
                flags['styleTest'] = True
                flags['compileTest'] = True
                flags['leaksTest'] = True
                flags['runtimeTest'] = True
            if arg == '--verterTest':
                flags['verterTest'] = True
            if arg == '--styleTest':
                flags['styleTest'] = True
            if arg == '--compileTest':
                flags['compileTest'] = True
            if arg == '--leaksTest':
                flags['leaksTest'] = True
            if arg == '--runtimeTest':
                flags['runtimeTest'] = True
            if arg == '--all':
                flags['all'] = True
        else:
            files.append(arg)
    return(files, flags)

def compileFile(name): 
    command = f'gcc -Werror -Wall -Wextra {name}.c -o {name}.out'
    command = run(command.split(), stdout=PIPE, stderr=STDOUT, text=True)
    return command

def formatFile(name): 
    command = f'clang-format -i {name}.c'
    command = run(command.split(), stdout=PIPE, stderr=STDOUT, text=True)
    return command

def styleTest(name): 
    command = f'clang-format -n {name}.c'
    command = run(command.split(), stdout=PIPE, stderr=STDOUT, text=True)
    return command

def runtimeTest(name): 
    command = f'cppcheck {name}.c'
    command = run(command.split(), stdout=PIPE, stderr=STDOUT, text=True)
    return command

def loadUnitTests(name):
    tests = {}
    with open(f'./{name}.test', 'r') as file:
        tests = {test.split(SEP)[0] : {'pred': test.split(SEP)[1], 'real': None, 'pass': False} for test in file.read().split(';')}
    file.close()
    return tests

def runVerterTests(name, tests): 
    for test in tests:
        command = run(f'./{name}.out'.split(), input=test, stdout=PIPE, stderr=STDOUT, text=True)
        tests[test]['real'] = command.stdout
        tests[test]['pass'] = tests[test]['pred'] == tests[test]['real']
    return tests

def printVerterTests(tests):
    cases = len(tests)
    passed = sum(map(lambda test: int(tests[test]['pass']) == True, tests))
    print(passed, cases)
    for test in tests:
        if not tests[test]['pass']:
            print('test:', test, 'output:', tests[test]['real'], 'pred:', tests[test]['pred'], 'ststus: FAIL')




if __name__ == '__main__':
    files, flags = parseArgv(sys.argv[1:])
    if flags['all']:
        files = getAllFiles()
    print(files)
    print(flags)
    # Format stage
    if flags['format']:
        print(".------------.")
        print("|FORMAT STAGE|")
        print("'------------'")
        for file in files:
            print(f'===> formating {file}.c <===')
            res = formatFile(file)
            print(res.stdout)
    # Compile stage
    if flags['compile']:
        print(".---------------.")
        print("|COMPILING STAGE|")
        print("'---------------'")
        for file in files:
            print(f'===> compiling {file}.c <===')
            res = compileFile(file)
            print(res.stdout)
    # Test stage
    # compileTest
    if flags['compileTest']:
        print(".--------------------.")
        print("|COMPILING TEST STAGE|")
        print("'--------------------'")
        for file in files:
            print(f'===> compile testing {file}.c <===')
            res = compileFile(file)
            print(res.stdout)
    # styleTest
    if flags['styleTest']:
        print(".----------------.")
        print("|STYLE TEST STAGE|")
        print("'----------------'")
        for file in files:
            print(f'===> style testing {file}.c <===')
            res = styleTest(file)
            print(res.stdout)
    # runtimeTest
    if flags['runtimeTest']:
        print(".------------------.")
        print("|RUNTIME TEST STAGE|")
        print("'------------------'")
        for file in files:
            print(f'===> runtime testing {file}.c <===')
            res = runtimeTest(file)
            print(res.stdout)   
    # verterTest
    if flags['verterTest']:
        print(".-----------------.")
        print("|VERTER TEST STAGE|")
        print("'-----------------'")
        for file in files:
            print(f'===> verter testing {file}.c <===')
            tests = loadUnitTests(file)
            tests = runVerterTests(file, tests)
            printVerterTests(tests)
    # leaksTest
    if flags['leaksTest']:
        print(".----------------.")
        print("|LEAKS TEST STAGE|")
        print("'----------------'")
        for file in files:
            print(f'===> leak testing {file}.c <===')
            tests = loadUnitTests(file)
    