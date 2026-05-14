/**
 * Teste de carga — Link Extractor (API direta).
 * Cada iteração = 10 invocações GET ao endpoint /api/<url> com URLs diferentes (enunciado).
 *
 * Variáveis de ambiente:
 *   BASE_URL     URL base da API (ex.: http://localhost:5000 ou http://localhost:4567)
 *   VUS          Número alvo de utilizadores virtuais (default: 10)
 *   RAMP_DURATION   Duração ramp-up (default: 30s)
 *   HOLD_DURATION   Duração em carga estável (default: 60s)
 *   PAUSE_MS     Pausa em ms entre cada um dos 10 pedidos (default: 0)
 *   SCENARIO     Etiqueta para o nome do ficheiro JSON exportado
 */
import http from "k6/http";
import { check, sleep } from "k6";
import { textSummary } from "https://jslib.k6.io/k6-summary/0.0.1/index.js";

const TARGET_URLS = [
  "http://example.com/",
  "https://example.org/",
  "https://www.w3.org/",
  "https://httpbin.org/",
  "https://httpbin.org/html",
  "https://www.debian.org/",
  "https://www.python.org/",
  "https://doc.rust-lang.org/stable/book/",
  "https://news.ycombinator.com/",
  "https://training.play-with-docker.com/",
];

const vus = parseInt(__ENV.VUS || "10", 10);
const ramp = __ENV.RAMP_DURATION || "30s";
const hold = __ENV.HOLD_DURATION || "60s";
const pauseSec = parseFloat(__ENV.PAUSE_MS || "0") / 1000;

export const options = {
  scenarios: {
    link_extractor: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: ramp, target: vus },
        { duration: hold, target: vus },
      ],
      gracefulRampDown: "15s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.99"],
  },
};

export default function () {
  const base = (__ENV.BASE_URL || "").replace(/\/$/, "");
  if (!base) {
    throw new Error("Defina BASE_URL (ex.: http://localhost:5000)");
  }

  for (const targetUrl of TARGET_URLS) {
    const path = `/api/${encodeURIComponent(targetUrl)}`;
    const res = http.get(`${base}${path}`, { timeout: "120s" });
    check(res, {
      "status 200": (r) => r.status === 200,
    });
    if (pauseSec > 0) {
      sleep(pauseSec);
    }
  }
}

export function handleSummary(data) {
  const scenario = __ENV.SCENARIO || "run";
  const stamp = Date.now();
  const jsonPath = `results/k6_${scenario}_${stamp}.json`;
  return {
    stdout: textSummary(data, { indent: " ", enableColors: true }),
    [jsonPath]: JSON.stringify(data, null, 2),
  };
}
