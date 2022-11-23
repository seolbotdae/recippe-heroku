<template>
  <v-card>
    <!-- 제목 부분 -->
    <v-card-title class="justify-center">
      {{ headerTitle }}
    </v-card-title>

    <!-- 내용 부분 -->
    <v-card-text class="text-center">
      <slot name="body">
        {{ defaultContent }}
      </slot>
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center mr-2 pb-4">
      <v-btn 
        color="#7895B2"
        small
        @click="$emit('hide')"
      >
        {{ btn1Title }}
      </v-btn>
      <template v-if="btn2">
        <v-btn
          color="#7895B2"
          small
          @click="$emit('submit')"
        >
          {{ btn2Title }}
        </v-btn>
      </template>
    </v-card-actions>

  </v-card>
</template>

<script>
export default{
  name: "Popup",
  data() {
    return {};
  },
  props: {
    headerTitle: {
      type: String,
      default: "제목",
    },
    defaultContent: {
      type: String,
      default: "내용",
    },
    btn1Title: {
      type: String,
      default: "닫기",
    },
    btn2: {
      type: Boolean,
      default: true
    },
    btn2Title: {
      type: String,
      default: "확인",
    }
  },
};
</script>