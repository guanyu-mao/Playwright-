import re
from .configure_dates import configure_dates
from .download_csv import download_csv

def loop_views(page):
    print("Starting loop_views...")  # Test line

    page.pause()
    print("Paused before selecting AccumulatedCosts VIEW")  # Test line

    # Use frame locator for all actions
    page.frame_locator('[id="_weave_e_271"] iframe').get_by_label("AccumulatedCosts").locator("div").filter(has_text="AccumulatedCosts VIEW").first.click()
    print("Clicked AccumulatedCosts VIEW")  # Test line

    page.pause()
    # Collect all option names before the loop
    options = page.frame_locator('[id="_weave_e_271"] iframe').get_by_role("option")
    option_count = options.count()
    option_names = [options.nth(i).inner_text() for i in range(option_count)]
    print(f"Found {option_count} options: {option_names}")

    for idx, view_name in enumerate(option_names):
        print(f"Processing view {idx+1}/{option_count}: {view_name}")

        # The dropdown button label is the previous view name, or "AccumulatedCosts" for the first round
        current_view_label = option_names[idx - 1] if idx > 0 else "AccumulatedCosts"

        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                # Click the dropdown button with the current view label
                page.frame_locator('[id="_weave_e_271"] iframe') \
                    .get_by_label(current_view_label) \
                    .locator("div").filter(has_text=f"{current_view_label} VIEW").first.click()
                print(f"Clicked dropdown for '{current_view_label}' (attempt {attempt+1})")

                # Wait for the option to be visible
                page.frame_locator('[id="_weave_e_271"] iframe') \
                    .get_by_role("option", name=view_name) \
                    .wait_for(state="visible", timeout=2000)
                print(f"Option '{view_name}' is visible.")
                break
            except Exception:
                print(f"Option '{view_name}' not visible, retrying dropdown (attempt {attempt+1})")
        else:
            print(f"Failed to make option '{view_name}' visible after {max_attempts} attempts, skipping.")
            continue

        # Click the option directly from the page object
        page.frame_locator('[id="_weave_e_271"] iframe') \
            .get_by_role("option", name=view_name).click(force=True)

        try:
            print(f"Calling configure_dates for view: {view_name}")
            configure_dates(page)
            print("configure_dates ran successfully")
        except Exception as e:
            print(f"Error in configure_dates: {e}")

        try:
            print(f"Calling download_csv for view: {view_name}")
            download_csv(page)
            print("download_csv ran successfully")
        except Exception as e:
            print(f"Error in download_csv: {e}")

print("Finished loop_views.")