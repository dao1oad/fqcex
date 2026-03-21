import { expect, test } from "@playwright/test";

test("shows readonly control-plane views for operator acceptance", async ({
  page,
}) => {
  await page.goto("/tradeability");

  await expect(page.getByRole("heading", { name: "Venue Tradeability" })).toBeVisible();
  await expect(page.locator(".status-card").filter({ hasText: "BYBIT" })).toBeVisible();
  await expect(page.getByRole("cell", { name: "BTC-USDT-PERP" }).first()).toBeVisible();

  await page.getByRole("link", { name: "Recovery" }).click();
  await expect(page.getByRole("heading", { name: "Recovery Runs" })).toBeVisible();
  await expect(page.getByText("reconciling balances")).toBeVisible();

  await page.getByRole("link", { name: "Audit" }).click();
  await expect(page.getByRole("heading", { name: "Audit Events" })).toBeVisible();
  await expect(page.getByText("approve_live_canary").first()).toBeVisible();
  await expect(page.getByText("corr-live-001").first()).toBeVisible();
});
