<template>
  <div class="relative inline-block">
    <svg
      :class="[InformationColorClass, 'w-7 h-7 ms-2 ']"
      aria-hidden="true"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      @mouseover="popoverMouseOver"
      @mouseleave="popoverMouseLeave"
      @click="popoverClick"
      ref="button"
    >
      <path
        fill-rule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
        clip-rule="evenodd"
      ></path>
    </svg>
    <div
      v-show="isPopoverVisible"
      ref="popover"
      @mouseover="popoverMouseOver"
      @mouseleave="popoverMouseLeave"
      :class="[
        positionClass,
        popoverColorClass,
        'fixed border-none rounded-lg shadow-lg p-4 w-96 popover',
      ]"
      :style="popoverStyle"
    >
      <h3
        class="text-lg font-semibold mb-2 dark:text-amber-400"
        v-html="popoverTitle"
      ></h3>
      <p class="text-gray-600 dark:text-white" v-html="popoverContent"></p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    position: {
      type: String,
      default: "top",
    },
    popoverColor: {
      type: String,
      default: "blue",
    },
    informationIconColor: {
      type: String,
      default: "blue",
    },
    trigger: {
      type: String,
      default: "mouseover",
    },
    popoverTitle: {
      type: String,
      default: "Popover Title",
    },
    popoverContent: {
      type: String,
      default:
        "This is the content of the popover. You can place any information here.",
    },
    isDarkMode: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isPopoverVisible: false,
      popoverStyle: {},
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    popoverMouseOver() {
      if (this.trigger === "mouseover") {
        this.showPopover();
      }
    },
    popoverMouseLeave() {
      if (this.trigger === "mouseover") {
        this.hidePopover();
      }
    },
    popoverClick() {
      if (this.trigger === "click") {
        this.isPopoverVisible ? this.hidePopover() : this.showPopover();
      }
    },
    showPopover() {
      this.isPopoverVisible = true;
      this.updatePopoverPosition();
    },
    hidePopover() {
      this.isPopoverVisible = false;
    },
    updatePopoverPosition() {
      this.$nextTick(() => {
        const button = this.$refs.button;
        const popover = this.$refs.popover;
        const buttonRect = button.getBoundingClientRect();
        const popoverRect = popover.getBoundingClientRect();
        const space = 4;

        let top, left;
        if (this.position === "top") {
          top = buttonRect.top - popoverRect.height - space;
          left = buttonRect.left + (buttonRect.width - popoverRect.width);
        } else if (this.position === "bottom") {
          top = buttonRect.bottom + space;
          left = buttonRect.left + (buttonRect.width - popoverRect.width) / 32;
        } else if (this.position === "left") {
          top = buttonRect.top + (buttonRect.height - popoverRect.height) / 32;
          left = buttonRect.left - popoverRect.width - space;
        } else if (this.position === "right") {
          top = buttonRect.top + (buttonRect.height - popoverRect.height) / 32;
          left = buttonRect.right + space;
        }

        this.popoverStyle = {
          top: `${top}px`,
          left: `${left}px`,
        };
      });
    },
  },
  computed: {
    positionClass() {
      return {
        top: "-translate-y-px",
        bottom: "translate-y-px",
        left: "-translate-x-px",
        right: "-translate-x-px",
      }[this.position];
    },
    popoverColorClass() {
      return {
        blue: "bg-blue-100 dark:bg-blue-900",
        slate: "bg-slate-800 dark:bg-slate-800",
        teal: "bg-teal-200 dark:bg-teal-900",
        cyan: "bg-cyan-200 dark:bg-cyan-900",
        sky: "bg-sky-200 dark:bg-sky-900",
      }[this.popoverColor];
    },

    InformationColorClass() {
      return {
        blue: "text-blue-700 hover:text-blue-800",
        slate: "text-slate-400 hover:text-slate-500 ",
        cyan: "text-cyan-700 hover:text-cyan-800 ",
        sky: "text-sky-700 hover:text-sky-800 ",
      }[this.informationIconColor];
    },
  },
};
</script>

<style scoped>
.popover {
  transition: opacity 0.2s;
}
</style>
