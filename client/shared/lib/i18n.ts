import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import enAssistant from "@/locales/en/assistant.json";
import enCommon from "@/locales/en/common.json";
import myAssistant from "@/locales/my/assistant.json";
import myCommon from "@/locales/my/common.json";

void i18n.use(initReactI18next).init({
  resources: {
    en: { common: enCommon, assistant: enAssistant },
    my: { common: myCommon, assistant: myAssistant },
  },
  lng: "my",
  fallbackLng: "en",
  supportedLngs: ["en", "my"],
  ns: ["common", "assistant"],
  defaultNS: "common",
  interpolation: { escapeValue: false },
});

export { i18n };
