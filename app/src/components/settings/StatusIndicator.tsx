import { Box, Loader } from "@mantine/core";
import { Check, X } from "lucide-react";
import { match } from "ts-pattern";

export type MutationStatus = "idle" | "pending" | "success" | "error";

/**
 * StatusIndicator component displays the status of a mutation operation.
 * Includes accessibility attributes (aria-label and role="status") for screen readers
 * to announce status changes.
 *
 * @param status - The current mutation status ("idle" | "pending" | "success" | "error")
 * @returns JSX element with appropriate icon and accessibility attributes, or null for idle state
 */
export function StatusIndicator({ status }: { status: MutationStatus }) {
	/**
	 * Helper function to create the wrapper Box with accessibility attributes.
	 * The role="status" makes it a live region that announces changes automatically.
	 *
	 * @param icon - The icon to display
	 * @param ariaLabel - The accessible label describing the current status
	 * @returns JSX Box element with icon and accessibility attributes
	 */
	const wrapper = (icon: React.ReactNode, ariaLabel: string) => (
		<Box
			style={{ display: "inline-flex", alignItems: "center" }}
			role="status"
			aria-label={ariaLabel}
		>
			{icon}
		</Box>
	);

	return match(status)
		.with("idle", () => null)
		.with("pending", () => wrapper(<Loader size="xs" />, "Saving..."))
		.with("success", () =>
			wrapper(
				<Check size={16} color="var(--mantine-color-green-6)" />,
				"Saved successfully",
			),
		)
		.with("error", () =>
			wrapper(
				<X size={16} color="var(--mantine-color-red-6)" />,
				"Save failed",
			),
		)
		.exhaustive();
}
