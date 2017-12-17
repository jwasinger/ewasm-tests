#! /usr/bin/env node

const evm2wasm = require('evm2wasm').evm2wasm
const evm2wast = require('evm2wasm').evm2wast
const process = require('process')

try {
  const argv = require('minimist')(process.argv.slice(2), {'string': 'code'})

  let evm = argv.code.toString()
  evm = evm.replace('0x', '')
  if (evm === '') {
    console.log('')
	  return
	}

  if ("wast" in argv) {
    let wast = evm2wast(evm)
    console.log(wast)
  } else {
    evm2wasm(evm).then((ewasm) => {
      console.log(Buffer.from(ewasm.buffer, 'hex').toString('hex'))
    }, (err) => {
      process.stderr.write(err)
    })
  }
} catch (e) {
  process.stderr.write(e)
  return
}
