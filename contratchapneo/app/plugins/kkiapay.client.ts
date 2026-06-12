// plugins/kkiapay.client.ts

import { defineNuxtPlugin } from "#app";
import * as kkiapayModule from "kkiapay";

export default defineNuxtPlugin(() => {
  return {
    provide: {
      kkiapay: kkiapayModule,
    },
  };
});