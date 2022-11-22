<template>
  <v-card>
    <v-card-title>
      {{ headerTitle }}
    </v-card-title>
    <v-card-text>
      <slot name="body">
        {{ defaultBodyContent }}
      </slot>
    </v-card-text>
    <v-card-actions class="justify-end mr-2 pb-4">
      <v-btn 
        color="amber"
        dark
        rounded
        small
        @click="$emit('hide')"
      >
        닫기
      </v-btn>
      <template v-if="btn2">
        <v-btn
          color="success"
          rounded
          small
          @click="$emit('submit')"
        >
          {{ btnTitle }}
        </v-btn>
      </template>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "Popup",
  data() {
    return {};
  },
  props: {
    btn2: {
      type: Boolean,
      default: true
    },
    headerTitle: {
      type: String,
      default: "제목",
    },
    btnTitle: {
      type: String,
      default: "확인",
    }
  },
};
</script>