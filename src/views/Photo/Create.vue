<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card height="800" color="#f5efe6">
          <v-btn flat class="ml-5 mt-5"> - 요리 사진 게시판</v-btn>
          <v-row>
              <v-col>
                <v-card fill-height color="#f5efe6" class="mt-10" flat>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 작성자 넣어주세요 -->
                        <v-card-title primary-title style="color:#7895B2">
                          작성자
                        </v-card-title>
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 이름 넣어주세요 -->
                        <v-card-title primary-title >
                          김재환
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat style="color:#7895B2">
                        <!-- 작성일 넣어주세요 -->
                        <v-card-title>
                          작성일
                        </v-card-title>
                        
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 날짜 넣어주세요 -->
                        <v-card-title primary-title>
                          2022/10/04 20:20:20
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
          </v-row>
          <v-file-input
            hide-input
            truncate-length="15"
          ></v-file-input>
          

          <div id="app">
            <input type="file" @change="onFileChange" />
          
            <div id="preview">
              <img v-if="url" :src="url"/>
            </div>
          </div>


        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default{
  data(){
    return{
      url:null
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    }
  }
}
</script>