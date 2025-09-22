import { version } from "./meta.ts";
import { parseArgs } from "jsr:@std/cli/parse-args";

function getFlags() {
  const flags = parseArgs(Deno.args, {
    string: ["help"],
  });
  return flags;
}

function initializeScriboProject(name: string) {
  console.log(`Initializing ${name}...`);
}
function buildScriboProject(name: string) {
  console.log(`Building ${name}...`);
}

function printHelp() {
  console.log(`\
usage: scribo [-h] [-i project_name] [-b project_dir] [-l project_dir] [--version]

Scribo is a static site generator.

options:
  -h, --help              show this help message and exit
  -i, --init project_name Initialize project
  -b, --build project_dir Build site for production
  --version               show program's version number and exit

Thank you for using scribo.
To contribute please visit https://github.com/sujaudd1n/scribo.
`);
}

if (import.meta.main) {
  const flags = getFlags();
  if (flags.init) {
    const projectName: string = flags.init;
    initializeScriboProject(projectName);
  } else if (flags.build) {
    const projectName: string = flags.build;
    buildScriboProject(projectName);
  } else if (flags.version) {
    console.log(version);
  } else {
    printHelp();
  }
}
