import APP_CONFIG from '../../app.config';

export class Node implements d3.SimulationNodeDatum {
  // Optional - defining optional implementation properties - required for relevant typing assistance
  index?: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;

  id: string;
  name: string;
  wikiLink: string;
  linkCount = 0;

  constructor(id, name, wikiLink) {
      this.id = id;
      this.name = name;
      this.wikiLink = wikiLink;
  }

  get r() {
    return APP_CONFIG.NODE_SIZE;
  }

  get fontSize() {
    return APP_CONFIG.FONT_SIZE;
  }

  get color() {
    // this is where influence can go
    return APP_CONFIG.SPECTRUM[1];
  }
}
