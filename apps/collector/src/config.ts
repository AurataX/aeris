// 62 OpenAQ reference monitors in Delhi NCR (same list as the S3 archive copy)
export const STATION_IDS = [
  17, 50, 235, 301, 5404, 5541, 5570, 5586, 5598, 5610, 5613, 5616, 5622, 5626, 5627, 5630, 5634, 5650, 5665,
  6356, 6358, 6359, 6924, 6929, 6931, 6932, 6934, 6936, 6938, 6953, 6957, 6960, 6972, 6978, 6980, 6986, 6988,
  7005, 8118, 8235, 8239, 8365, 8472, 8475, 8915, 8917, 10484, 10485, 10486, 10488, 10820, 10825, 10831, 10900,
  10908, 10919, 10920, 10921, 11603, 11607, 3409519, 3410004,
];

export const CPCB_STATES = ["Delhi", "Haryana", "Uttar Pradesh"];
export const CPCB_RESOURCE = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69";

// the free Worker plan allows 50 subrequests per run, so stations are split into two halves
export const half = (n: number) => STATION_IDS.filter((_, i) => i % 2 === n);

export const CITIES: Record<string, [number, number]> = {
  Delhi: [28.6139, 77.209],
  Gurugram: [28.4595, 77.0266],
  Noida: [28.5355, 77.391],
  Ghaziabad: [28.6692, 77.4538],
  Faridabad: [28.4089, 77.3178],
};

export const WEATHER_VARS =
  "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,surface_pressure";
