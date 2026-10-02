// Each fortune has its own printed lucky numbers.
const FORTUNES = [
  { text: "The best times of your life have not yet been lived.", lucky: [41, 36, 22, 51, 39, 34] },
  { text: "You are free to invent your life.", lucky: [8, 21, 33, 53, 42, 7] },
  { text: "A mysterious stranger will enter your life and change everything.", lucky: [15, 39, 40, 36, 27, 37] },
  { text: "Your luck will completely change today.", lucky: [36, 54, 47, 50, 52, 32] },
  { text: "Your mind is filled with new ideas, explore them.", lucky: [49, 50, 38, 29, 16, 1] },
  { text: "Your ability to find the silly in the serious will take you far.", lucky: [40, 6, 8, 19, 7, 29] },
  { text: "One who admires you greatly is hidden before your eyes.", lucky: [1, 53, 44, 32, 54, 21] },
  { text: "A single kind word can keep one warm for years.", lucky: [14, 26, 17, 23, 52, 25] },
  { text: "To conquer your flaws, you must first accept them.", lucky: [48, 33, 41, 5, 47, 22] },
  { text: "The stars appear every night in the sky. All is well.", lucky: [6, 36, 35, 19, 52, 30] },
  { text: "The simplest answer is to act.", lucky: [10, 42, 46, 53, 37, 20] },
  { text: "Nothing is impossible to a willing heart.", lucky: [2, 46, 24, 53, 30, 28] },
  { text: "Embrace the healing power of music, and you’ll find solace in its embrace.", lucky: [6, 26, 38, 36, 32, 8] },
  { text: "Nurture the garden of your mind with positive thoughts.", lucky: [28, 33, 52, 49, 39, 32] },
  { text: "Hope is the most precious treasure to a person.", lucky: [26, 34, 17, 27, 37, 31] },
  { text: "Your dreams are never silly; depend on them to guide you.", lucky: [33, 34, 52, 2, 37, 15] },
  { text: "You will soon be surrounded by good friends and laughter.", lucky: [50, 9, 53, 4, 46, 34] },
  { text: "It’s up to you to make the next move.", lucky: [43, 7, 46, 40, 28, 31] },
  { text: "Keep an eye open for opportunity.", lucky: [10, 31, 15, 8, 41, 45] },
  { text: "Take the chance while you still have the choice.", lucky: [30, 44, 31, 46, 35, 17] },
  { text: "All the efforts you’re making will ultimately pay off.", lucky: [36, 26, 43, 20, 55, 42] },
];

// How many cookies are in the bag each day.
const PER_DAY = 8;
