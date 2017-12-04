#! /usr/bin/env node

const evm2wasm = require('evm2wasm').evm2wasm
const evm2wast = require('evm2wasm').evm2wast
const process = require('process')
const argv = require('minimist')(process.argv.slice(2))

if (!Object.keys(argv).includes("code")) {
  process.stderr.write("missing required argument --code")
  process.exit(-1)
}

let evm = argv.code.toString()

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
