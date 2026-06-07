# Fixture: complex diff

This fixture simulates a PR diff containing a deeply nested, multi-responsibility Python function
with a high branching factor and SQL injection vulnerabilities via f-string interpolation.

Use this fixture for eval 5 — evaluating Code complexity and Security scoring.

---

```diff
diff --git a/pipeline/record_processor.py b/pipeline/record_processor.py
index 0000000..1234abc 100644
--- /dev/null
+++ b/pipeline/record_processor.py
@@ -0,0 +1,98 @@
+def process_record(record, config, db_conn, cache, logger, dry_run=False):
+    result = {}
+    if record:
+        if record.get("type") == "transaction":
+            if record.get("amount") is not None:
+                if record["amount"] > 0:
+                    if config.get("validate"):
+                        if record.get("merchant_id"):
+                            merchant = db_conn.query(
+                                f"SELECT * FROM merchants WHERE id = '{record['merchant_id']}'"
+                            )
+                            if merchant:
+                                if merchant[0].get("active"):
+                                    result["merchant"] = merchant[0]
+                                    if config.get("enrich"):
+                                        enriched = cache.get(record["merchant_id"])
+                                        if enriched:
+                                            result["enriched"] = enriched
+                                        else:
+                                            logger.debug("Cache miss — fetching from DB")
+                                            enriched = db_conn.query(
+                                                f"SELECT * FROM merchant_meta WHERE merchant_id = '{record['merchant_id']}'"
+                                            )
+                                            if enriched:
+                                                result["enriched"] = enriched[0]
+                                                cache.set(record["merchant_id"], enriched[0])
+                                else:
+                                    logger.warning("Merchant inactive")
+                                    result["status"] = "rejected"
+                                    return result
+                            else:
+                                logger.error("Merchant not found")
+                                result["status"] = "error"
+                                return result
+                        else:
+                            logger.warning("Missing merchant_id")
+                            result["status"] = "invalid"
+                            return result
+                    if not dry_run:
+                        try:
+                            db_conn.execute(
+                                f"INSERT INTO transactions VALUES ('{record['id']}', '{record['amount']}', '{record.get('merchant_id', '')}')"
+                            )
+                            result["status"] = "committed"
+                        except Exception as e:
+                            logger.error(f"Insert failed: {e}")
+                            result["status"] = "failed"
+                    else:
+                        result["status"] = "dry_run"
+                else:
+                    result["status"] = "zero_amount"
+            else:
+                result["status"] = "null_amount"
+        elif record.get("type") == "refund":
+            if record.get("original_transaction_id"):
+                original = db_conn.query(
+                    f"SELECT * FROM transactions WHERE id = '{record['original_transaction_id']}'"
+                )
+                if original:
+                    if original[0].get("status") == "committed":
+                        if record.get("amount") <= original[0].get("amount"):
+                            if config.get("validate"):
+                                if record.get("reason"):
+                                    if len(record["reason"]) > 5:
+                                        if not dry_run:
+                                            db_conn.execute(
+                                                f"INSERT INTO refunds VALUES ('{record['id']}', '{record['original_transaction_id']}', '{record['amount']}')"
+                                            )
+                                            result["status"] = "refund_committed"
+                                        else:
+                                            result["status"] = "dry_run"
+                                    else:
+                                        result["status"] = "reason_too_short"
+                                else:
+                                    result["status"] = "missing_reason"
+                            else:
+                                if not dry_run:
+                                    db_conn.execute(
+                                        f"INSERT INTO refunds VALUES ('{record['id']}', '{record['original_transaction_id']}', '{record['amount']}')"
+                                    )
+                                    result["status"] = "refund_committed"
+                        else:
+                            result["status"] = "refund_exceeds_original"
+                    else:
+                        result["status"] = "original_not_committed"
+                else:
+                    result["status"] = "original_not_found"
+            else:
+                result["status"] = "missing_original_id"
+        else:
+            result["status"] = "unknown_type"
+    else:
+        result["status"] = "empty_record"
+    return result
```
