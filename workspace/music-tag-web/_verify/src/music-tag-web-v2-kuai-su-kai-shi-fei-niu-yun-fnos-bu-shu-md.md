> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md).

# 飞牛云fnos部署

fnos版本：0.8.24

官网地址：<http://www.musictagweb.com/>

进入docker界面搜索 xhongc/music\_tag\_web 点击下载

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FVH7tTRPiis1wjlaoaXt7%2FSnipaste_2024-12-04_21-37-21.png?alt=media&amp;token=d7a4e618-c6a0-4d15-8f8b-0b019419d42a" alt=""><figcaption></figcaption></figure>

选择对应版本：latest

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F7chjAR5Q7dBVNLXr17bE%2FSnipaste_2024-12-04_21-38-02.png?alt=media&amp;token=3630e78a-3465-4ade-8a2c-57b87ad5309c" alt=""><figcaption></figcaption></figure>

等待下载完成

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F2VHqtswOYeHE7Xy3CL33%2FSnipaste_2024-12-04_21-38-54.png?alt=media&amp;token=ee7145f5-26aa-47a0-8d90-95e6438e109e" alt=""><figcaption></figcaption></figure>

两种方式可以部署，二选一

第一种：容器部署

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FuBqovbYUgCKbm45JjSVy%2FSnipaste_2024-12-04_22-35-37.png?alt=media&amp;token=e6af00ab-7727-4797-b0ff-8e8a90bfdb35" alt=""><figcaption></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FrdmL3Wrno5jETUc5DHSU%2FSnipaste_2025-06-03_11-00-29.png?alt=media&amp;token=a1779cc9-782c-4c48-b0ec-cd7449dad01b" alt=""><figcaption></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FddkI18yiJ1G2McCU0pNc%2Fimage.png?alt=media&amp;token=3b905405-a765-43f1-bb43-2c976229b0e2" alt=""><figcaption></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FzFnKe5kFHQK8IuLvmoqP%2FSnipaste_2024-12-04_22-38-56.png?alt=media&amp;token=c8d30f0b-d9fc-4369-8e9b-5e5ea40a6291" alt=""><figcaption></figcaption></figure>

成功部署访问8002端口，默认账号密码 都为 admin，左上角V1标签点击激活V2版本

第二种：Compose部署

<div><figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FGL1cc1Vhe3oKJ51GUhap%2FSnipaste_2024-12-04_22-46-18.png?alt=media&amp;token=184c9457-73f0-4c0c-945a-85a7b907e363" alt=""><figcaption></figcaption></figure> <figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FVnmn1mFUWN6kIZ1mSyop%2FSnipaste_2024-12-04_22-49-27.png?alt=media&amp;token=5f9b83d0-7ff6-42c7-a21b-43be88827d32" alt=""><figcaption></figcaption></figure> <figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FJzARETy0sFDHal5MWAyp%2FSnipaste_2024-12-04_22-49-33.png?alt=media&amp;token=f1a99f8f-9fa7-4433-b4b6-3f991bc8cb56" alt=""><figcaption></figcaption></figure></div>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FnVHCdDgjM4NDtIqKvnzD%2FSnipaste_2024-12-04_22-48-05.png?alt=media&amp;token=f453807e-926e-4515-aa57-3a4b4fc9b297" alt=""><figcaption></figcaption></figure>
