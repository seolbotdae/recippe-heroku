<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" fill-height color="#f5efe6">
          <v-btn text class="ml-5 mt-5"> - 요리 사진 게시판</v-btn>
          <v-row>
              <v-col>
                <v-card fill-height color="#f5efe6" class="mt-10" flat>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
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
          
          <v-row >
            <v-col justify="center">
              <v-card v-if="preview" >
                <v-img :src="preview" class="img-fluid" contain/>
                <p class="mb-0">file name: {{ image.name }}</p>
                <p class="mb-0">size: {{ image.size/1024 }}KB</p>
              </v-card>
              <input type="file" accept="image/*" @change="previewImage" class="form-control-file" id="my-file">
      
            </v-col>
          </v-row>

          <v-card height="300" color="#f5efe6" flat id="card-on-off">
          </v-card>

          <v-row>
            <v-col offset="5" col="2">
              <v-btn x-large color="#7895B2">게시글 게시</v-btn>
            </v-col>
          </v-row>


        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default{
  data(){
    return {
      preview: null,
      image: null,
      preview_list: [],
      image_list: []
    };
  },
  methods: {
    previewImage: function(event) {
      const btn1 = document.getElementById('card-on-off')
      if(btn1.style.display !== 'none') {
        btn1.style.display = 'none';
      }


      var input = event.target;
      if (input.files) {
        var reader = new FileReader();
        reader.onload = (e) => {
          this.preview = e.target.result;
        }
        this.image=input.files[0];
        reader.readAsDataURL(input.files[0]);
      }
    },
    reset: function() {
      this.image = null;
      this.preview = null;
      this.image_list = [];
      this.preview_list = [];
    }
  }
}

</script>