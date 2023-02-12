const cp = require('child_process')

if (process.env.NODE_ENV !== 'production') {
  process.on('uncaughtException', (err) => {
    const match = String(err).match(/Cannot find module '(.*)'/)
    if (match && !match[1].startsWith('.')) {
      const install = cp.spawnSync('npm', ['i', match[1], '-S'], { stdio: "inherit", encoding : 'utf8' })
      if (install.stderr) {
        console.error(install.stderr)
      }
      if (install.stdout) {
        console.log(install.stdout)
      }
    } else {
      console.error(err)
    }
  })
}
