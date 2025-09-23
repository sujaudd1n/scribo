import * as path from "@std/path";
import { copy, exists, walk } from "@std/fs";
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

async function buildScriboProject(projectName: string) {
  const projectRoot: string = path.relative(Deno.cwd(), projectName);
  if (!await exists(projectRoot, { isDirectory: true })) {
    console.log(
      `Project ${projectName} not found. Please enter valid project path. Exiting...`,
    );
    Deno.exit(1);
  }
  console.log(projectRoot);
  Deno.chdir(projectRoot);

  console.log(`Building ${projectName}...`);
  const walkObj = await Array.fromAsync(walk("."));
  if (await exists("dist")) {
    await Deno.remove("dist", { recursive: true });
  }
  for (let wo of walkObj) {
    if (!wo.path.startsWith("pages")) {
      continue;
    }
    if (wo.isDirectory) {
      const inputDirName: string = wo.path;
      const distDir: string = path.join(
        "dist",
        ...inputDirName.split("/").slice(1),
      );
      Deno.mkdir(distDir);
    } else if (wo.isFile) {
      console.log(wo)
      let parsedFile = path.parse(wo.path);
      console.log(parsedFile.dir.split(path.SEPARATOR).slice(1));
      const outputFile = path.join(
        "dist",
        ...parsedFile.dir.split(path.SEPARATOR).slice(1),
        parsedFile.name + ".html",
      );
      console.log(outputFile);
      await copy(wo.path, outputFile)
    }
  }
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
