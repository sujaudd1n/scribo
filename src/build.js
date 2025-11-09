import * as path from "@std/path";
import { copy, exists, walk } from "@std/fs";
import nunjucks from "nunjucks";
import { marked } from "npm:marked"
import os from "node:os"

const homedir = os.homedir()
const templates_dir = `${homedir}/.local/share/scribo/templates`
nunjucks.configure(templates_dir, { autoescape: false });
nunjucks.render("index.html", { html: "hello" });

const DIST_DIR_NAME = "dist";

export async function buildScriboProject(projectPath) {
  if (!await exists(projectPath, { isDirectory: true })) {
    console.log(
      `Project ${projectPath} not found. Please enter valid project path. Exiting...`,
    );
    Deno.exit(1);
  }

  console.log(`Building ${projectPath}...`);

  const dist_dir = `${projectPath}/${DIST_DIR_NAME}`;
  if (await exists(dist_dir)) {
    console.log(`${dist_dir} exists. Deleting...`);
    await Deno.remove(dist_dir, { recursive: true });
  }

  await copy(`${projectPath}/pages`, dist_dir);

  const links = [];
  const renderData = []

  const walkObj = await Array.fromAsync(walk(dist_dir));
  for (let wo of walkObj) {
    if (wo.isDirectory) {
      continue;
    } else if (wo.isFile) {
      // get file source
      const parsedFile = path.parse(wo.path);
      const { dir, name } = parsedFile;
      if (name.startsWith(".")) continue
      // generate output file content
      const markdownText = await Deno.readTextFile(wo.path);
      const htmlFilePath = path.join(dir, name + ".html");
      console.log("htmlfilename", htmlFilePath)
      links.push({ name: name, path: trimPath(htmlFilePath) })
      // render template and save
      // const htmlText = nunjucks.render("index.html", {
      //   html: marked.parse(markdownText),
      //   contents: links
      // });

      renderData.push({
        path: htmlFilePath,
        html: marked.parse(markdownText)
      })

      await Deno.remove(wo.path);

    }
  }


  for (let data of renderData) {
    await Deno.writeTextFile(data.path, nunjucks.render("index.html", {
      html: data.html,
      contents: links
    }));
  }

  await copy(`${templates_dir}/script.js`, path.join(dist_dir, "script.js"));
  await copy(`${templates_dir}/style.css`, path.join(dist_dir, "style.css"));

  // await copy(`${import.meta.dirname}/templates/script.js`, path.join(dist_dir, ""));
  console.log("Build successful.");
}


function trimPath(path) {
  const params = path.split("/").slice(2)
  const newPath = params.join("/")
  return newPath

}