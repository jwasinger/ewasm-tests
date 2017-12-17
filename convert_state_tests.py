import os, glob, sys, subprocess, json, pdb

def evm2wasm(code):
  result = subprocess.run(['./convert.js', '--code', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  error = result.stderr.decode('utf-8')
  if error != '':
    raise Exception(error)

  return result.stdout.decode('utf-8').strip('\n')

def convert_state_test(file_name):
  state_test = None

  with open(file_name, 'r') as f:
    try:
      state_test = json.load(f)
    except Exception as e:
      print("{0}: {1}".format(file_name, e))
      return
    
  if not state_test:
    print("foo")
    sys.exit(-1)

  for test_case in state_test.keys():
    # conver pre account code
    for addr in state_test[test_case]['pre']:
      if state_test[test_case]['pre'][addr]['code'] != '':
        state_test[test_case]['pre'][addr]['code'] = '0x'+evm2wasm(state_test[test_case]['pre'][addr]['code'])

    if state_test[test_case]['transaction']['data'] != '':
      for i in range(0, len(state_test[test_case]['transaction']['data'])):
        state_test[test_case]['transaction']['data'][i] = '0x'+evm2wasm(state_test[test_case]['transaction']['data'][i])

  with open(file_name, 'w') as f:
    f.write(json.dumps(state_test, indent=4, sort_keys=True))
    
STATE_TEST_PATH = os.path.join(os.getcwd(), 'tests/GeneralStateTests')

for file_name in glob.iglob(STATE_TEST_PATH+'/**/*.json', recursive=True):
  convert_state_test(file_name)
