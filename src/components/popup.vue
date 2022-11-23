<template>
  <div>
    
    <v-row justify="center">
      <v-col cols="10">
        {{ headerTitle }}
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="10">
        <slot name="body">
          {{ defaultContent }}
        </slot>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="3">
        <v-btn 
          color="#7895B2"
          small
          @click="$emit('hide')"
        >
          {{ btnTitle }}
        </v-btn>
      </v-col>
      <v-col  cols="3">
        <template v-if="btn2">
          <v-btn
            color="#7895B2"
            small
            @click="$emit('submit')"
          >
            {{ btn2Title }}
          </v-btn>
        </template>
      </v-col>
    </v-row>

  </div>
</template>

<script>
export default {
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
    btnTitle: {
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