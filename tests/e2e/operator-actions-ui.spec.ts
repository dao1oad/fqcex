import { expect, test } from "@playwright/test";

test("enforces operator action preconditions and echoes accepted actions into audit", async ({
  page,
}) => {
  await page.goto("/actions");

  await expect(page.getByRole("heading", { name: "Operator Actions" })).toBeVisible();

  await page.getByLabel("Target").selectOption("OKX:BTC-USDT-PERP");
  await page.getByLabel("Action").selectOption("force_resume");
  await page.getByLabel("Reason").fill("resume after live gate review");

  await expect(page.getByText("approvalRecorded").first()).toBeVisible();
  await expect(page.getByRole("button", { name: "Submit Action" })).toBeDisabled();

  await page.getByLabel("Target").selectOption("BINANCE:ETH-USDT-PERP");
  await expect(page.getByRole("button", { name: "Submit Action" })).toBeEnabled();
  await page.getByRole("button", { name: "Submit Action" }).click();

  await expect(
    page.locator(".nested-card").filter({ hasText: "force_resume" }),
  ).toBeVisible();
  await expect(
    page.locator(".nested-card").filter({ hasText: "corr-action-001" }),
  ).toBeVisible();

  await page.getByRole("link", { name: "Audit" }).click();
  await expect(page.getByRole("heading", { name: "Audit Events" })).toBeVisible();
  await expect(
    page.locator(".timeline-card").filter({ hasText: "force_resume" }).first(),
  ).toBeVisible();
  await expect(page.getByText("corr-action-001").first()).toBeVisible();
});
