<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" color="#f5efe6">

          <!-- 정렬 아이콘 -->
          <v-row>
            <v-col offset="10">
              <span class="sort-base">Edit</span>
            
              <v-btn class="ml-5">
                <v-icon >
                  mdi-format-list-bulleted
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>

          <v-row justify="center">
            <v-col cols="8">
              <v-card height="400" v-for="item in list" class="my-10">
                <v-row>
                  <v-col class="d-flex justify-space-between">
                    <div class="pl-5">
                      <v-card-title>{{item.title}}</v-card-title>
                      <v-card-subtitle>{{item.date}}</v-card-subtitle> 
                    </div>
                    <div>
                      <v-icon class="pa-6" large>
                        mdi-thumb-up-outline
                      </v-icon>
                      <span class="pr-6 like-count">{{item.like}}</span>
                    </div>
                  </v-col>
                </v-row>

                <v-row justify="center">
                  <v-col cols="8">
                    <v-img
                      lazy-src="https://w.namu.la/s/45e2317ae59261dcc8643bfa26897a253a3162b145e770687fcf649e461a99ae3b87401baf461913986519a8ed951db7d5f477222a5fe09d8d0b1c6c988e33c97e4d25588755b598af2025a04d3a3fc4b0c149cc3fdfa702f71ae970575d19ef"
                      contain
                      src="https://w.namu.la/s/45e2317ae59261dcc8643bfa26897a253a3162b145e770687fcf649e461a99ae3b87401baf461913986519a8ed951db7d5f477222a5fe09d8d0b1c6c988e33c97e4d25588755b598af2025a04d3a3fc4b0c149cc3fdfa702f71ae970575d19ef"
                    ></v-img>
                  </v-col>
                </v-row>
                  
                
                
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
.sort-base{
  font-size: 1.2em;
}

.like-count{
  font-size: 1.6em;
}
</style>

<script>
export default{
  data(){
    return {
      list : [
        {
          title: "hello1",
          date :"2022/02/03",
          like : 3
        
        },
        {
          title:"hello2",
          date:"2020/03/04",
          like : 3
        },
        {
          title:"hello3",
          date:"2020/03/04",
          like : 3
        },
        {
          title:"hello4",
          date:"2020/03/04",
          like : 3
        },
        {
          title:"hello5",
          date:"2020/03/04",
          like : 3
        }
      ]
    };
  },
  methods: {}
  
}
</script>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default {
  data () {
    return {
      photo: [],
      photoID: null
    }
  },
  mounted() {
    let vm = this;
    herokuAPI.photoList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.photoList[i] != null; i++) {
              vm.photo.push(response.data.photoList[i]);
            }
          }
      })
  },
  methods: {
    toLookup(photoID) {
      router.push({
        path: "/photo/lookup/"+photoID,
      })
    }
  }
}
</script>