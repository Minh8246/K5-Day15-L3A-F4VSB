import { fileURLToPath } from "node:url";

export default {
  agentRules: false,
  devIndicators: false,
  turbopack: { root: fileURLToPath(new URL(".", import.meta.url)) },
};
