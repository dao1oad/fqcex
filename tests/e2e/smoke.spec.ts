import { expect, test } from "@playwright/test";
import path from "node:path";
import { pathToFileURL } from "node:url";

test("loads the smoke fixture", async ({ page }) => {
  const fixturePath = path.resolve(__dirname, "fixtures", "index.html");
  const fixtureUrl = pathToFileURL(fixturePath).href;

  await page.goto(fixtureUrl);

  await expect(page).toHaveTitle(/perp-platform smoke fixture/i);
  await expect(
    page.getByRole("heading", { name: "perp-platform smoke fixture" }),
  ).toBeVisible();
  await expect(page.getByTestId("smoke-status")).toHaveText("deploy scaffold ready");
  await expect(page.getByTestId("rollback-status")).toHaveText(
    "explicit rollback path defined",
  );
});
