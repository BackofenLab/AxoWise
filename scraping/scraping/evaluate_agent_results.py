import json
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def convert_to_binary_labels(gt_set, pred_set, all_items):
    """ convert sets to binary labels for sklearn metrics """
    y_true = [1 if item in gt_set else 0 for item in all_items]
    y_pred = [1 if item in pred_set else 0 for item in all_items]
    return y_true, y_pred

def get_field(data, field_path):
    """ Safely get a field from nested dictionary """
    current = data
    for key in field_path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current

def evaluate_accession_codes(gt_codes, pred_codes):
    # if either is None, we can't compare
    if gt_codes is None and pred_codes is None:
        return None
    
    # if one is None but not the other, treat the None as empty dict
    gt_codes = gt_codes or {}
    pred_codes = pred_codes or {}
    
    def normalize_codes(codes):
        """ convert dictionary of lists into a set of accession codes """
        normalized = set()
        for accessions in codes.values():
            # handle if accessions is a list or single item
            if isinstance(accessions, list) and accessions:
                normalized.update(acc for acc in accessions)
            elif isinstance(accessions, str):
                normalized.add(accessions)
        return normalized
    
    # convert both to sets of accession numbers only
    gt_set = normalize_codes(gt_codes)
    pred_set = normalize_codes(pred_codes)
    
    all_items = gt_set.union(pred_set)
    
    if not all_items:  # empty case
        return {
            "accuracy": 1.0,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0
        }
    
    y_true, y_pred = convert_to_binary_labels(gt_set, pred_set, all_items)
    
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=1),
        "recall": recall_score(y_true, y_pred, zero_division=1),
        "f1": f1_score(y_true, y_pred, zero_division=1)
    }

def evaluate_seqdata_srccode(gt_list, pred_list):
    # if both are None, we can't compare
    if gt_list is None and pred_list is None:
        return None
    
    # if one is None but not the other, treat the None as empty list
    gt_list = gt_list or []
    pred_list = pred_list or []
    
    def normalize_item(item):
        """Convert item to a hashable type"""
        if isinstance(item, list):
            return tuple(normalize_item(x) for x in item)
        else:
            return str(item)  # Convert to string for comparison
    
    gt_set = {normalize_item(item) for item in gt_list}
    pred_set = {normalize_item(item) for item in pred_list}
    all_items = gt_set.union(pred_set)
    
    if not all_items:  # handle empty case
        return {
            "accuracy": 1.0,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0
        }
    
    y_true, y_pred = convert_to_binary_labels(gt_set, pred_set, all_items)
    
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=1),
        "recall": recall_score(y_true, y_pred, zero_division=1),
        "f1": f1_score(y_true, y_pred, zero_division=1)
    }

def pair_articles(ground_truth, predictions):
    """ pair ground truth and prediction articles by DOI """
    paired_data = []
    for gt_item in ground_truth:
        for pred_item in predictions:
            if (gt_item.get("DOI") == pred_item.get("DOI")):
                paired_data.append((gt_item, pred_item))
                break
    return paired_data

def evaluate_results(ground_truth_path, prediction_path):
    """ main evaluation function that processes both files and returns metrics"""    
    ground_truth = load_json(ground_truth_path)
    predictions = load_json(prediction_path)
    
    # initialize results
    results = defaultdict(list)
    
    # pair documents
    paired_data = pair_articles(ground_truth, predictions)
    
    # evaluate each pair
    for gt_item, pred_item in paired_data:
        gt_acc_codes = get_field(gt_item, ["results", "accession_codes"])
        pred_acc_codes = get_field(pred_item, ["results", "accession_codes"])
        
        gt_seq_data = get_field(gt_item, ["results", "sequencing_data"])
        pred_seq_data = get_field(pred_item, ["results", "sequencing_data"])
        
        gt_src_code = get_field(gt_item, ["results", "source_code"])
        pred_src_code = get_field(pred_item, ["results", "source_code"])
        
        # evaluate accession codes if either exists
        acc_metrics = evaluate_accession_codes(gt_acc_codes, pred_acc_codes)
        if acc_metrics is not None:
            results["accession_codes"].append(acc_metrics)
        
        # evaluate sequencing data if either exists
        seq_metrics = evaluate_seqdata_srccode(gt_seq_data, pred_seq_data)
        if seq_metrics is not None:
            results["sequencing_data"].append(seq_metrics)
        
        # evaluate source code if either exists
        src_metrics = evaluate_seqdata_srccode(gt_src_code, pred_src_code)
        if src_metrics is not None:
            results["source_code"].append(src_metrics)
    
    # calculate average metrics for each category
    final_results = {}
    
    for category, metrics_list in results.items():
        if not metrics_list:
            final_results[category] = {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0
            }
            continue
            
        avg_accuracy = sum(m["accuracy"] for m in metrics_list) / len(metrics_list)
        avg_precision = sum(m["precision"] for m in metrics_list) / len(metrics_list)
        avg_recall = sum(m["recall"] for m in metrics_list) / len(metrics_list)
        avg_f1 = sum(m["f1"] for m in metrics_list) / len(metrics_list)
        
        final_results[category] = {
            "accuracy": avg_accuracy,
            "precision": avg_precision,
            "recall": avg_recall,
            "f1": avg_f1
        }
    
    return final_results

def save_results(results, output_path):
    """Save evaluation results by appending to existing entries"""
    try:
        with open(output_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]
            
            # Get the last entry which should be from the current execution
            current_entry = data[-1]
            
            # Update the last entry with accuracy results
            current_entry.update({
                "accession_codes": results.get("accession_codes", {}),
                "sequencing_data": results.get("sequencing_data", {}),
                "source_code": results.get("source_code", {})
            })
            
            # Write back the entire updated list
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
                
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist, create new entry
        with open(output_path, 'w') as f:
            json.dump([{
                "run_number": 1,
                "execution_time": 0,  # placeholder
                "accession_codes": results.get("accession_codes", {}),
                "sequencing_data": results.get("sequencing_data", {}),
                "source_code": results.get("source_code", {})
            }], f, indent=2)

def evaluate():
    results = evaluate_results(
        ground_truth_path="file_test.json",
        prediction_path="file_output.json"
    )
    
    # print results in a formatted way
    print("\nEvaluation Results:")
    print("-" * 50)

    for category in ["accession_codes", "sequencing_data", "source_code"]:
        if category not in results:
            print(f"\n{category.upper()}: No data available")
            continue
            
        print(f"\n{category.upper()}:")
        print(f"Accuracy:  {results[category]['accuracy']:.4f}")
        print(f"Precision: {results[category]['precision']:.4f}")
        print(f"Recall:    {results[category]['recall']:.4f}")
        print(f"F1-Score:  {results[category]['f1']:.4f}")
        
    save_results(results, "evaluation_results.json")

if __name__ == "__main__":
    evaluate()