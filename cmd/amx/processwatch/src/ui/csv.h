/* Copyright (C) 2022 Intel Corporation */
/* SPDX-License-Identifier: GPL-2.0-only */

#pragma once

#include <math.h>
#include <inttypes.h>

static void print_csv_header(FILE *csv_file) {
  int i;
  
  if(!csv_file) return;
  
  fprintf(csv_file, "interval,pid,name,");
  for(i = 0; i < pw_opts.cols_len; i++) {
    fprintf(csv_file, "%s", get_name(pw_opts.cols[i]));
    if(i != (pw_opts.cols_len - 1))  {
      fprintf(csv_file, ",");
    }
  }
  fprintf(csv_file, "\n");
}

static void print_csv_interval(FILE *csv_file) {
  int i, n, counter;
  process_t *process;
  
  if(!csv_file) return;
  
  /* Print overall first */
  fprintf(csv_file, "%" PRIu64 ",", results->interval_num);
  fprintf(csv_file, "%s,", "ALL");
  fprintf(csv_file, "%s,", "ALL");
  for(i = 0; i < pw_opts.cols_len; i++) {
    fprintf(csv_file, "%lf", get_interval_percent(pw_opts.cols[i]));
    if(i != (pw_opts.cols_len - 1))  {
      fprintf(csv_file, ",");
    }
  }
  fprintf(csv_file, "\n");
  
  /* Now one line per process */
  counter = 0;
  for(i = 0; i < results->interval->pid_ctr; i++) {
    process = get_interval_process_info(results->interval->pids[i]);
    if(!process) continue;
    if(!get_interval_proc_num_samples(i)) continue;
    counter++;
    fprintf(csv_file, "%" PRIu64 ",", results->interval_num);
    fprintf(csv_file, "%d,", results->interval->pids[i]);
    fprintf(csv_file, "%s,", process->name);
    for(n = 0; n < pw_opts.cols_len; n++) {
      fprintf(csv_file, "%lf", get_interval_proc_percent(process->index, pw_opts.cols[n]));
      if(n != (pw_opts.cols_len - 1))  {
        fprintf(csv_file, ",");
      }
    }
    fprintf(csv_file, "\n");
  }
  if(counter) {
    fprintf(csv_file, "\n");
  }
}
