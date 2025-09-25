import * as path from "@std/path";
import { copy, exists, walk } from "@std/fs";
import nunjucks from "nunjucks";

nunjucks.configure("html_templates");
nunjucks.render("index.html", { html: "hello" });

const DIST_DIR_NAME = "dist";

export async function buildScriboProject(projectPath: string) {
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

  const walkObj = await Array.fromAsync(walk(dist_dir));
  for (let wo of walkObj) {
    if (wo.isDirectory) {
      continue;
    } else if (wo.isFile) {
      const parsedFile = path.parse(wo.path);
      const { dir, name } = parsedFile;
      console.log(dir, name, wo.path);
      const markdownText = await Deno.readTextFile(wo.path);
      const htmlText = nunjucks.render("index.html", {
        html: markdownText,
      });
      const htmlFileName = path.join(dir, name + ".html");
      // console.log("htmlfilename", htmlFileName)
      await Deno.writeTextFile(htmlFileName, htmlText);
      await Deno.remove(wo.path);
    }
  }

  await copy(`${import.meta.dirname}/assets`, path.join(dist_dir, "assets"));
  console.log("Build successful.");
}
