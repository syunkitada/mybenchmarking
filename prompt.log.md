# Prompt Log

1. .github/CONSTITUTION.md を作成する

以下のプロンプトで、.github/CONSTITUTION.md を作成します。

このプロジェクトにおいて何に重点を置くかをざっくり指定します。

今回は、まず動くこと、テストは最小限でよいこと、階層化された小さなモジュール郡で構成されることとしています。

```
/speckit.specify Create principles focused on "Working First", "Minimal Testing", "Layered small modules"
```

2. .specify/SPEC.md を作成する

以下のプロンプトで、.specify/SPEC.md を作成します。

```
/speckit.specify Build an linux server benchmark toolkit.
This toolkit provides documentation on how to run existing benchmark tools such as sysbench and fio and how to interpret the results.
It also provides tools for analyzing those benchmark results and custom benchmark tools.
```

その後、以下のようなプロンプトで SPEC.md の内容を調整していきます。

```
このツールキットの主な目的はシステムベンチマークのためのドキュメンテーションです。
CPU、メモリ、ディスク、ネットワークのベンチマークツールの利用方法をまとめることです。
また私のPCのベンチマーク結果を保存しておき、結果を解析できるようにすることです。
これを踏まえて、SPEC.mdを書き換えてください。
```

```
Result Storageは、jsonファイルベースのシンプルな作りとし、このリポジトリにそのまま保存します。
Github上にそのまま生のデータとを保存したいです。
これを踏まえて、SPEC.mdを書き換えてください。
```

3. 再調整

```
.github/CONSTITUTION.md の内容を要約し、必要に応じて改善してください。
```

```
.specify/SPEC.md の内容を要約し、必要に応じて改善してください。
```

```
HW/OSなどの不変なSystem情報は分離して管理できるようにします。Systemの中にはVM(qemu)も存在します。
一方で、kernelパラメータやソフトウェアパラメータの細かな違いを記録できるようにします。
これを踏まえて、SPEC.mdを書き換えてください。
```

```
.specify/SPEC.md 内の日本語を英語で記述し直してください。
```

4. Planing

```
/speckit.plan The application uses Python. Use uv.
```

5. Generate tasks

```
/speckit.tasks
```

6. Implement

```
/speckit.implement
```

一回で完了しないので、tasks.md のチェックが埋まってくまで何度か実行します。

```
/speckit.implement
```
