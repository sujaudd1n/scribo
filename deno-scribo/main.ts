import * as path from "@std/path";
import { copy, exists } from "@std/fs";
import { parseArgs } from "@std/cli";
import { version } from "./meta.ts";

function getFlags() {
  const flags = parseArgs(Deno.args, {
    string: ["init", "build", "help"],
    boolean: ["version"],
  });
  return flags;
}

async function initializeScriboProject(projectName: string) {
  const projectRoot: string = path.join(import.meta.dirname, projectName);
  if (await exists(projectRoot, { isDirectory: true })) {
    console.log(
      `Project ${projectName} already exists in the current working directory. Exiting...`,
    );
    Deno.exit(1);
  }
  console.log(`Initializing ${name}...`);
  await copy("skeleton", projectRoot);
  console.log(`Project ${projectName} has been initialized.`);
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
  } else if (Object.prototype.hasOwnProperty.call(flags, "build")) {
    const projectName: string = flags.build;
    if (projectName === "") {
      console.log("Please use valid project name.");
      Deno.exit(1);
    }
    buildScriboProject(projectName);
  } else if (flags.version) {
    console.log(version);
  } else {
    printHelp();
  }
}
