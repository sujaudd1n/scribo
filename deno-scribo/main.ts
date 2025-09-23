import { version } from "./meta.ts";
import { parseArgs } from "@std/cli";

function getFlags() {
  const flags = parseArgs(Deno.args, {
    string: ["init", "build", "help"],
    boolean: ["version", "v"],
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
  if (Object.prototype.hasOwnProperty.call(flags, "init")) {
    const projectName: string = flags.init;
    if (projectName === "") {
      console.log("Please use valid project name.");
      Deno.exit(1);
    }
    initializeScriboProject(projectName);
  } else if (flags.build) {
    const projectName: string = flags.build;
    buildScriboProject(projectName);
  } else if (flags.version || flags.v) {
    console.log(version);
  } else {
    printHelp();
  }
}
