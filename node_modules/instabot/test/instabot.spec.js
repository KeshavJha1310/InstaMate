'use strict'
import test from 'ava'
import cp from 'child_process'

test.cb('installs missing module', (t) => {
  process.on = (evName, cb) => {
    t.is(evName, 'uncaughtException')

    t.notThrows(() => {
      cb(new Error("random err"))
    })
    t.notThrows(() => {
      cb(new Error("Cannot find module 'koa'"))
    })
  }
  cp.spawnSync = (command, args, opts) => {
    t.is(command, 'npm')
    t.is(args[0], 'i')
    t.is(args[1], 'koa')

    t.end()
    return {
      stderr: 'stderr',
      stdout: 'stdout'
    }
  }
  require('../instabot')
})
